"""PayPal API Client."""
# -*- coding: utf-8 -*-


from csv import DictReader
from datetime import datetime, timedelta
from typing import Callable, Generator

import httpx
import singer

API_SCHEME: str = 'https://'
API_BASE_URL_LIVE: str = 'ca-live.adyen.com'
API_BASE_URL_TEST: str = 'ca-test.adyen.com'
API_PATH_REPORTS: str = '/reports/download'
API_PATH_REPORTS_COMPANY: str = '/Company/:company:'
API_PATH_REPORTS_MERCHANT: str = '/MerchantAccount/:merchant:'
API_PATH_DISPUTE_REPORT: str = '/dispute_report_:date:.csv'
API_PATH_PAYMENT_REPORT: str = '/payments_accounting_report_:date:.csv'
API_PATH_SETTLEMENT_REPORT: str = '/settlement_detail_report_batch_:batch:.csv'


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
        self.base_url = API_BASE_URL_TEST if self.istest else API_BASE_URL_LIVE

        # Replace Placeholder in reports path
        merchant = API_PATH_REPORTS_MERCHANT.replace(
            ':merchant:',
            self.merchant_account,
        )
        while True:
            report = API_PATH_SETTLEMENT_REPORT.replace(
                ':batch:',
                str(batch_number),
            )
            # Create the URL
            url: str = (
                f'{API_SCHEME}{self.base_url}'
                f'{API_PATH_REPORTS}'
                f'{merchant}'
                f'{report}'
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
        self.base_url = API_BASE_URL_TEST if self.istest else API_BASE_URL_LIVE

        # Parse start_date string to date
        parsed_date = datetime.strptime(start_date, '%Y-%m-%d')

        # Replace Placeholder in reports path
        company = API_PATH_REPORTS_COMPANY.replace(
            ':company:',
            self.company_account,
        )
        while True:
            date = parsed_date.strftime('%Y_%m_%d')
            report = API_PATH_DISPUTE_REPORT.replace(
                ':date:',
                str(date),
            )
            # Create the URL
            url: str = (
                f'{API_SCHEME}{self.base_url}'
                f'{API_PATH_REPORTS}'
                f'{company}'
                f'{report}'
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
        self.base_url = API_BASE_URL_TEST if self.istest else API_BASE_URL_LIVE

        # Replace Placeholder in reports path
        merchant = API_PATH_REPORTS_MERCHANT.replace(
            ':merchant:',
            self.merchant_account,
        )

        # Parse start_date string to date
        parsed_date = datetime.strptime(start_date, '%Y-%m-%d')

        while True:
            date = parsed_date.strftime('%Y_%m_%d')
            report = API_PATH_PAYMENT_REPORT.replace(
                ':date:',
                str(date),
            )
            # Create the URL
            url: str = (
                f'{API_SCHEME}{self.base_url}'
                f'{API_PATH_REPORTS}'
                f'{merchant}'
                f'{report}'
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
