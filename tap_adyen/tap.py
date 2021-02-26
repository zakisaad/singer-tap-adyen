"""Adyen tap."""
# -*- coding: utf-8 -*-
import logging
from argparse import Namespace

import pkg_resources
from singer import get_logger, utils
from singer.catalog import Catalog

from tap_adyen.adyen import Adyen
from tap_adyen.discover import discover
from tap_adyen.sync import sync

VERSION: str = pkg_resources.get_distribution('tap-adyen').version
LOGGER: logging.RootLogger = get_logger()
REQUIRED_CONFIG_KEYS: tuple = (
    'start_date',
    'report_user',
    'company_account',
    'user_password',
    'merchant_account',
)


@utils.handle_top_exception(LOGGER)
def main() -> None:
    """Run tap."""
    # Parse command line arguments
    args: Namespace = utils.parse_args(REQUIRED_CONFIG_KEYS)

    LOGGER.info(f'>>> Running tap-adyen v{VERSION}')

    # If discover flag was passed, run discovery mode and dump output to stdout
    if args.discover:
        catalog: Catalog = discover()
        catalog.dump()
        return

    # Otherwise run in sync mode
    if args.catalog:
        # Load command line catalog
        catalog = args.catalog
    else:
        # Loadt the  catalog
        catalog = discover()

    # Initialize Adyen client
    adyen: Adyen = Adyen(
        args.config['report_user'],
        args.config['company_account'],
        args.config['user_password'],
        args.config['merchant_account'],
        args.config.get('test', False),
    )

    sync(adyen, args.state, catalog, args.config['start_date'])


if __name__ == '__main__':
    main()
