"""Tools."""
# -*- coding: utf-8 -*-

from datetime import timedelta
from typing import Optional, Union

from dateutil.parser import parse as parse_date


def clear_currently_syncing(state: dict) -> dict:
    """Clear the currently syncing from the state.

    Arguments:
        state (dict) -- State file

    Returns:
        dict -- New state file
    """
    return state.pop('currently_syncing', None)


def get_stream_state(state: dict, tap_stream_id: str) -> dict:
    """Return the state of the stream.

    Arguments:
        state {dict} -- The state
        tap_stream_id {str} -- The id of the stream

    Returns:
        dict -- The state of the stream
    """
    return state.get(
        'bookmarks',
        {},
    ).get(tap_stream_id)


def get_bookmark_value(
    stream_name: str,
    csv_url: str,
) -> Optional[Union[str, int]]:
    """Retrieve bookmark value from the csv url.

    Arguments:
        stream_name {str} -- Stream name
        csv_url {str} -- Csv url

    Returns:
        Optional[Union[str, int]] -- [description]
    """
    if stream_name in {'dispute_transaction_details', 'payment_accounting'}:
        # Return the date +1 day
        return str(
            parse_date(
                csv_url.rstrip('.csv'),
                fuzzy=True,
            ).date() + timedelta(days=1),
        )
    elif stream_name == 'settlement_details':
        # Return the batch number + 1
        return int(csv_url.rstrip('.csv').rpartition('_')[2]) + 1
    return None
