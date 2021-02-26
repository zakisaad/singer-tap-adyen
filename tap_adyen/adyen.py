"""PayPal API Client."""
# -*- coding: utf-8 -*-


from csv import DictReader
from datetime import datetime, timedelta
from typing import Callable, Generator

import httpx
import singer

API_SCHEME: str = 'https://'
API_BASE_URL: str = 'ca-live.adyen.com/reports/download/MerchantAccount/'
API_BASE_URL_COMPANY: str = 'ca-live.adyen.com/reports/download/Company/'
API_TEST_URL: str = 'ca-test.adyen.com/reports/download/MerchantAccount/'
API_TEST_URL_COMPANY: str = 'ca-test.adyen.com/reports/download/Company/'
API_SETTLEMENT_REPORT_NAME: str = '/settlement_detail_report_batch_'
API_PAYMENT_REPORT_NAME: str = '/payments_accounting_report_'
API_DISPUTE_REPORT_NAME: str = '/dispute_report_'
API_FILE_EXTENTION: str = '.csv'


class Adyen(object):
    """Adyen API Client."""

    def __init__(  # noqa: WPS211
        self,
        report_user: str,
        company_account: str,
        user_password: str,
        merchant_account: str,
        test: bool,
    ) -> None:
        """Initialize client.

        Arguments:
            report_user {str} -- Reporting User Username
            company_account {str} -- Adyen Company Account
            user_password {str} -- Reporing User API Key
            merchant_account {str} -- Adyen Merchant Account
            test {bool} -- determine if the live or test env needs to be used
        """
        self.report_user: str = report_user
        self.company_account: str = company_account
        self.user_password: str = user_password
        self.merchant_account: str = merchant_account
        self.istest: bool = test

        self.logger = singer.get_logger()

    def settlement_details(
        self,
        batch_number: int,
    ) -> Generator[str, None, None]:
        """Get the Settlement Detail Report URLS.

        Arguments:
            batch_number {int} -- batch number to start generating urls from

        Yields:
            url {str} -- (working) url of settlement detail reports
        """
        # Check what URL to use (test/live)
        api_url = self.iftest(self.istest)
        while True:
            # Create the URL
            url: str = (
                f'{API_SCHEME}{api_url}'
                f'{self.merchant_account}'
                f'{API_SETTLEMENT_REPORT_NAME}'
                f'{batch_number}{API_FILE_EXTENTION}'
            )

            # Check if the created URL returns a 200 status code
            response = self.head_request(url)
            if response.status_code == 200:  # noqa: WPS432
                self.logger.info(f'Found: Report {batch_number}')
                # Yield the URL
                yield url
                batch_number += 1
            elif response.status_code == 404:  # noqa: WPS432
                self.logger.debug(f'No report number {batch_number} found')
                break
            else:
                self.logger.critical('Unexpected status code')
                response.raise_for_status()
        self.logger.info('Finished Settlement Detail Reports')

    def dispute_transaction_details(
        self,
        start_date: str,
    ) -> Generator[str, None, None]:
        """Get the Dispute Transaction Report URLS.

        Arguments:
            start_date {str} -- starting date to start generating urls from

        Yields:
            url {str} -- (working) url of dispute transaction reports
        """
        # Check what URL to use (test/live)
        if self.istest is True:
            api_url = API_TEST_URL_COMPANY
        else:
            api_url = API_BASE_URL_COMPANY

        # Parse start_date string to date
        parsed_date = datetime.strptime(start_date, '%Y-%m-%d')

        while True:
            date = parsed_date.strftime('%Y_%m_%d')
            # Create the URL
            url: str = (
                f'{API_SCHEME}{api_url}'
                f'{self.company_account}'
                f'{API_DISPUTE_REPORT_NAME}'
                f'{date}{API_FILE_EXTENTION}'
            )
            # Check if the created URL returns a 200 status code
            response = self.head_request(url)
            if response.status_code == 200:  # noqa: WPS432
                self.logger.info(f'Found: Report {date}')
                # Yield the URL
                yield url
                parsed_date = parsed_date + timedelta(days=1)
            elif response.status_code == 404:  # noqa: WPS432
                self.logger.debug(f'No report number {date} found')
                break
            else:
                self.logger.critical('Unexpected status code')
                response.raise_for_status()
        self.logger.info('Finished Dispute Transaction Reports')

    def payment_accounting(
        self,
        start_date: str,
    ) -> Generator[str, None, None]:
        """Get the Payment Accounting Report URLS.

        Arguments:
            start_date {str} -- starting date to start generating urls from

        Yields:
            url {str} -- (working) url of payment accounting reports
        """
        # Check what URL to use (test/live)
        api_url = self.iftest(self.istest)

        # Parse start_date string to date
        parsed_date = datetime.strptime(start_date, '%Y-%m-%d')

        while True:
            date = parsed_date.strftime('%Y_%m_%d')
            # Create the URL
            url: str = (
                f'{API_SCHEME}{api_url}'
                f'{self.merchant_account}'
                f'{API_PAYMENT_REPORT_NAME}'
                f'{date}{API_FILE_EXTENTION}'
            )

            # Check if the created URL returns a 200 status code
            response = self.head_request(url)
            if response.status_code == 200:  # noqa: WPS432
                self.logger.info(f'Found: Report {date}')
                # Yield the URL
                yield url
                parsed_date = parsed_date + timedelta(days=1)
            elif response.status_code == 404:  # noqa: WPS432
                self.logger.debug(f'No report number {date} found')
                break
            else:
                self.logger.critical('Unexpected status code')
                response.raise_for_status()
        self.logger.info('Finished Payment Accounting Reports')

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
        self.logger.info(f'Downloading: report {csv_url}')

        # Get Request to get the csv in binary format
        client: httpx.Client = httpx.Client(http2=True)

        response: httpx._models.Response = client.get(  # noqa: WPS437
            csv_url,
            auth=(self.report_user, self.user_password),
        )

        # If the status is 200 raise the status
        if response.status_code != 200:  # noqa: WPS432
            self.logger.critical('Unexpected status code')
            response.raise_for_status()

        # Put the split lines in a dictionary
        settlements = DictReader(response.text.splitlines(), delimiter=',')

        # Clean dictionary and yield every settlement
        if cleaner:
            yield from (
                cleaner(settlement, row_number)
                for row_number, settlement in enumerate(settlements)
            )
        # Return every settlement if no cleaner exists
        else:
            yield from (
                settlement
                for settlement in settlements
            )
        self.logger.info(f'Finished: report {csv_url}')

    def head_request(self, url: str):
        """Return headers of url.

        Arguments:
            url {str} -- url to request the headers from

        Returns:
            reponse {httpx.Response} -- headers of url
        """
        client: httpx.Client = httpx.Client(http2=True)
        response: httpx._models.Response = client.head(  # noqa: WPS437
            url,
            auth=(self.report_user, self.user_password),
        )
        return response

    def iftest(self, test: bool):
        if test is True:
            return API_TEST_URL
        if test is False:
            return API_BASE_URL
