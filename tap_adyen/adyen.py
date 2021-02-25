"""PayPal API Client."""
# -*- coding: utf-8 -*-


import singer
from typing import Callable, Generator
from tap_adyen.cleaners import clean_settlement_details
from csv import DictReader
import httpx


API_SCHEME: str = 'https://'
API_BASE_URL: str = 'ca-live.adyen.com/reports/download/MerchantAccount/'
API_SETTLEMENT_REPORT_NAME: str = '/settlement_detail_report_batch_'
API_FILE_EXTENTION: str = '.csv'


class Adyen(object):
    """Adyen API Client."""

    def __init__(
        self,
        report_user: str,
        company_account: str,
        user_password: str,
        merchant_account: str,
    ) -> None:
        """Initialize client.

        Arguments:
            report_user {str} -- Reporting User Username
            company_account {str} -- Adyen Company Account
            user_password {str} -- Reporing User API Key
            merchant_account {str} -- Adyen Merchant Account
        """
        self.report_user: str = report_user
        self.company_account: str = company_account
        self.user_password: str = user_password
        self.merchant_account: str = merchant_account

        self.logger = singer.get_logger()


    def settlement_details(self, batch_number: int):
        # Start with batch numer
        # while True
            # Build url strinng
            # .get = Download pagina
            # .head = headers only
            # If status_code == 200
                # yield
                # Batch +=1 
            # else
                # raise StopItt



    def settlement_details_old(
        self,
        **kwargs: dict,
    ) -> Generator[dict, None, None]:
        """Adyen settlement details report.

        Raises:
            ValueError: When the parameter start_batch is missing

        Yields:
            Generator[dict] -- Yields Adyen Settlement Details
        """

        self.logger.info('Stream Adyen Settlement Detail Report')

        # Validate the batch_number value exist if not, raise error
        batch_input: str = str(kwargs.get('batch_number', ''))

        if not batch_input:
            raise ValueError('The parameter batch_number is required.')

        self.logger.info(
            f'Retrieving transactions from batch number {batch_input}',
        )

        # Build URL
        url: str = (
            f'{API_SCHEME}{API_BASE_URL}'
            f'{self.merchant_account}'
            f'{API_SETTLEMENT_REPORT_NAME}'
            f'{batch_input}{API_FILE_EXTENTION}'
        )

        self.logger.info('Downloading report from ' + url)

        # Get Request to get the csv in binary format
        client: httpx.Client = httpx.Client(http2=True)

        response: httpx._models.Response = client.get(  # noqa: WPS437
            url,
            auth=(self.report_user, self.user_password),
        )
        # Check if it finds the report
        if response.status_code != 200:  # noqa: WPS432
            raise ValueError('Report not found')

        # Put the split lines in a dictionary
        settlements = DictReader(response.text.splitlines(), delimiter=',')

        # Clean dictionary and yield every settlement
        yield from (
            clean_settlement_details(settlement, row)
            for row, settlement in enumerate(settlements)
        )
        self.logger.info('Finished: Adyen settlement_details')


    def get_csv(self, csv_url: str, cleaner: Callable):
        # Get CSV
        # Dict Reader
        # If cleaner
            #    Yield cleaner(settlement, row_number)
        # else yield settlement
