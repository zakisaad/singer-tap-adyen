"""Sync data."""
# -*- coding: utf-8 -*-
import logging
from datetime import datetime, timezone
from typing import Callable, Optional, Union

import singer
from singer.catalog import Catalog, CatalogEntry

from tap_adyen import tools
from tap_adyen.adyen import Adyen
from tap_adyen.cleaners import CLEANERS
from tap_adyen.streams import STREAMS

LOGGER: logging.RootLogger = singer.get_logger()


def sync(  # noqa: WPS210
    adyen: Adyen,
    state: dict,
    catalog: Catalog,
    start_date: str,
) -> None:
    """Sync data from tap source.

    Arguments:
        adyen {Adyen} -- Adyen client
        state {dict} -- Tap state
        catalog {Catalog} -- Stream catalog
        start_date {str} -- Start date
    """
    # For every stream in the catalog
    LOGGER.info('Sync')
    LOGGER.debug('Current state:\n{state}')

    # Only selected streams are synced, whether a stream is selected is
    # determined by whether the key-value: "selected": true is in the schema
    # file.
    for stream in catalog.get_selected_streams(state):
        LOGGER.info(f'Syncing stream: {stream.tap_stream_id}')

        # Update the current stream as active syncing in the state
        singer.set_currently_syncing(state, stream.tap_stream_id)

        # Retrieve the state of the stream
        stream_state: dict = tools.get_stream_state(
            state,
            stream.tap_stream_id,
        )

        LOGGER.debug(f'Stream state: {stream_state}')

        # Write the schema
        singer.write_schema(
            stream_name=stream.tap_stream_id,
            schema=stream.schema.to_dict(),
            key_properties=stream.key_properties,
        )

        # Every stream has a corresponding method in the Adyen object e.g.:
        # The stream: settlement_details will call: adyen.settlement_details
        tap_urls: Callable = getattr(adyen, stream.tap_stream_id)

        # The tap_urls method yields urls to CSVs. The state of the stream is
        # used as kwargs for the method.
        # E.g. if the state of the stream has a key 'start_date', it will be
        # used in the method as start_date='2021-01-01T00:00:00+0000'
        for csv_url in tap_urls(**stream_state):

            # Retrieve the cleaner function
            cleaner: Optional[Callable] = CLEANERS.get(stream.tap_stream_id)

            bookmark_value: Optional[Union[str, int]] = None
            # Retrieve the csv
            for row in adyen.get_csv(csv_url, cleaner):

                # Write a row to the stream
                singer.write_record(
                    stream.tap_stream_id,
                    row,
                    time_extracted=datetime.now(timezone.utc),
                )
                # Update bookmark value
                bookmark_value = tools.retrieve_bookmark_with_path(
                    stream.replication_key,
                    row,
                )

            # Update bookmark
            update_bookmark(stream, bookmark_value, state)


def update_bookmark(
    stream: CatalogEntry,
    bookmark_value: Optional[Union[str, int]],
    state: dict,
) -> None:
    """Update the bookmark.

    Arguments:
        stream {CatalogEntry} -- Stream catalog
        bookmark_value {Optional[Union[str, int]]} -- Record
        state {dict} -- State
    """
    # Retrieve the value of the bookmark
    if bookmark_value:
        # Save the bookmark to the state
        singer.write_bookmark(
            state,
            stream.tap_stream_id,
            STREAMS[stream.tap_stream_id]['bookmark'],
            bookmark_value,
        )

    # Clear currently syncing
    tools.clear_currently_syncing(state)

    # Write the bootmark
    singer.write_state(state)
