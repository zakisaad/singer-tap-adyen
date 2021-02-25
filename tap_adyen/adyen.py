"""PayPal API Client."""
# -*- coding: utf-8 -*-


from csv import DictReader
from typing import Callable, Generator

import httpx
import singer

API_SCHEME: str = 'https://'
API_BASE_URL: str = 'ca-live.adyen.com/reports/download/MerchantAccount/'
API_TEST_URL: str = 'ca-test.adyen.com/reports/download/MerchantAccount/'
API_SETTLEMENT_REPORT_NAME: str = '/settlement_detail_report_batch_'
API_FILE_EXTENTION: str = '.csv'


class Adyen(object):
    """Adyen API Client."""

    def __init__(  # noqa: WPS211
        self,
        report_user: str,
        user_password: str,
        merchant_account: str,
        company_account: str,
        test: bool,
    ) -> None:
        """Initialize client.

        Arguments:
            report_user {str} -- Reporting User Username
            user_password {str} -- Reporing User API Key
            merchant_account {str} -- Adyen Merchant Account
            company_account {str} -- Adyen Company Account
            test {bool} -- determine if the live or test env needs to be used
        """
        self.report_user: str = report_user
        self.user_password: str = user_password
        self.merchant_account: str = merchant_account
        self.istest: bool = test

        self.logger = singer.get_logger()

    def settlement_details(
        self,
        batch_number: int,
    ) -> Generator[str, None, None]:
        """Initialize client.

        Arguments:
            batch_number {int} -- batch number to start generating urls from

        Yields:
            url {str} -- (working) url of settlement detail reports
        """
        # Check what URL to use (test/live)
        if self.istest is True:
            api_url = API_TEST_URL
        else:
            api_url = API_BASE_URL

        while True:
            # Create the URL
            url: str = (
                f'{API_SCHEME}{api_url}'
                f'{self.merchant_account}'
                f'{API_SETTLEMENT_REPORT_NAME}'
                f'{batch_number}{API_FILE_EXTENTION}'
            )

            # Check if the created URL returns a 200 status code
            client: httpx.Client = httpx.Client(http2=True)
            response: httpx._models.Response = client.head(  # noqa: WPS437
                url,
                auth=(self.report_user, self.user_password),
            )

            if response.status_code == 200:  # noqa: WPS432
                self.logger.info(
                    f'Found Report with number {batch_number}',
                )
                # Yield the URL
                yield url
                batch_number += 1
            else:
                break

    def get_csv(
        self,
        csv_url: str,
        cleaner: Callable,
    ) -> Generator[dict, None, None]:
        """Download csv.

        Arguments:
            csv_url {str} -- The URL that points to the correct CSV file

        Yields:
            Generator[dict] -- Yields Adyen CSV's
        """
        self.logger.info('Downloading report from ' + csv_url)

        # Get Request to get the csv in binary format
        client: httpx.Client = httpx.Client(http2=True)

        response: httpx._models.Response = client.get(  # noqa: WPS437
            csv_url,
            auth=(self.report_user, self.user_password),
        )

        # Put the split lines in a dictionary
        settlements = DictReader(response.text.splitlines(), delimiter=',')

        # Clean dictionary and yield every settlement
        if cleaner:
            yield from (
                cleaner(settlement, row_number)
                for row_number, settlement in enumerate(settlements)
            )
        else:
            yield from (
                settlement
                for settlement in settlements
            )
        self.logger.info('Finished: Adyen settlement_details')
