"""Streams metadata."""
# -*- coding: utf-8 -*-
from datetime import datetime
from decimal import Decimal
from types import MappingProxyType

from dateutil.parser import parse as parse_date

# Helper constants for timezone parsing
HOUR: int = 3600
TIMEZONES: MappingProxyType = MappingProxyType({
    'A': HOUR,
    'ACDT': 10.5 * HOUR,  # noqa: WPS432
    'ACST': 9.5 * HOUR,  # noqa: WPS432
    'ACT': -5 * HOUR,  # noqa: WPS432
    'ACWST': 8.75 * HOUR,  # noqa: WPS432
    'ADT': 4 * HOUR,  # noqa: WPS432
    'AEDT': 11 * HOUR,  # noqa: WPS432
    'AEST': 10 * HOUR,  # noqa: WPS432
    'AET': 10 * HOUR,
    'AFT': 4.5 * HOUR,  # noqa: WPS432
    'AKDT': -8 * HOUR,
    'AKST': -9 * HOUR,
    'ALMT': 6 * HOUR,  # noqa: WPS432
    'AMST': -3 * HOUR,  # noqa: WPS432
    'AMT': -4 * HOUR,  # noqa: WPS432
    'ANAST': 12 * HOUR,  # noqa: WPS432
    'ANAT': 12 * HOUR,  # noqa: WPS432
    'AQTT': 5 * HOUR,  # noqa: WPS432
    'ART': -3 * HOUR,
    'AST': 3 * HOUR,  # noqa: WPS432
    'AT': -4 * HOUR,
    'AWDT': 9 * HOUR,  # noqa: WPS432
    'AWST': 8 * HOUR,  # noqa: WPS432
    'AZOST': 0,
    'AZOT': -1 * HOUR,
    'AZST': 5 * HOUR,
    'AZT': 4 * HOUR,
    'AoE': -12 * HOUR,  # noqa: WPS432
    'B': 2 * HOUR,
    'BNT': 8 * HOUR,
    'BOT': -4 * HOUR,
    'BRST': -2 * HOUR,
    'BRT': -3 * HOUR,
    'BST': 6 * HOUR,
    'BTT': 6 * HOUR,
    'C': 3 * HOUR,
    'CAST': 8 * HOUR,
    'CAT': 2 * HOUR,
    'CCT': 6.5 * HOUR,  # noqa: WPS432
    'CDT': -5 * HOUR,
    'CEST': 2 * HOUR,
    'CET': HOUR,
    'CHADT': 13.75 * HOUR,  # noqa: WPS432
    'CHAST': 12.75 * HOUR,  # noqa: WPS432
    'CHOST': 9 * HOUR,
    'CHOT': 8 * HOUR,
    'CHUT': 10 * HOUR,
    'CIDST': -4 * HOUR,
    'CIST': -5 * HOUR,
    'CKT': -10 * HOUR,
    'CLST': -3 * HOUR,
    'CLT': -4 * HOUR,
    'COT': -5 * HOUR,
    'CST': -6 * HOUR,
    'CT': -6 * HOUR,
    'CVT': -1 * HOUR,
    'CXT': 7 * HOUR,
    'ChST': 10 * HOUR,
    'D': 4 * HOUR,
    'DAVT': 7 * HOUR,
    'DDUT': 10 * HOUR,
    'E': 5 * HOUR,
    'EASST': -5 * HOUR,
    'EAST': -6 * HOUR,
    'EAT': 3 * HOUR,
    'ECT': -5 * HOUR,
    'EDT': -4 * HOUR,
    'EEST': 3 * HOUR,
    'EET': 2 * HOUR,
    'EGST': 0,
    'EGT': -1 * HOUR,
    'EST': -5 * HOUR,
    'ET': -5 * HOUR,
    'F': 6 * HOUR,
    'FET': 3 * HOUR,
    'FJST': 13 * HOUR,  # noqa: WPS432
    'FJT': 12 * HOUR,  # noqa: WPS432
    'FKST': -3 * HOUR,
    'FKT': -4 * HOUR,
    'FNT': -2 * HOUR,
    'G': 7 * HOUR,
    'GALT': -6 * HOUR,
    'GAMT': -9 * HOUR,
    'GET': 4 * HOUR,
    'GFT': -3 * HOUR,
    'GILT': 12 * HOUR,  # noqa: WPS432
    'GMT': 0,
    'GST': 4 * HOUR,
    'GYT': -4 * HOUR,
    'H': 8 * HOUR,
    'HDT': -9 * HOUR,
    'HKT': 8 * HOUR,
    'HOVST': 8 * HOUR,
    'HOVT': 7 * HOUR,
    'HST': -10 * HOUR,
    'I': 9 * HOUR,
    'ICT': 7 * HOUR,
    'IDT': 3 * HOUR,
    'IOT': 6 * HOUR,
    'IRDT': 4.5 * HOUR,  # noqa: WPS432
    'IRKST': 9 * HOUR,
    'IRKT': 8 * HOUR,
    'IRST': 3.5 * HOUR,  # noqa: WPS432
    'IST': 5.5 * HOUR,  # noqa: WPS432
    'JST': 9 * HOUR,
    'K': 10 * HOUR,
    'KGT': 6 * HOUR,
    'KOST': 11 * HOUR,  # noqa: WPS432
    'KRAST': 8 * HOUR,
    'KRAT': 7 * HOUR,
    'KST': 9 * HOUR,
    'KUYT': 4 * HOUR,
    'L': 11 * HOUR,  # noqa: WPS432
    'LHDT': 11 * HOUR,  # noqa: WPS432
    'LHST': 10.5 * HOUR,  # noqa: WPS432
    'LINT': 14 * HOUR,  # noqa: WPS432
    'M': 12 * HOUR,  # noqa: WPS432
    'MAGST': 12 * HOUR,  # noqa: WPS432
    'MAGT': 11 * HOUR,  # noqa: WPS432
    'MART': 9.5 * HOUR,  # noqa: WPS432
    'MAWT': 5 * HOUR,
    'MDT': -6 * HOUR,
    'MHT': 12 * HOUR,  # noqa: WPS432
    'MMT': 6.5 * HOUR,  # noqa: WPS432
    'MSD': 4 * HOUR,
    'MSK': 3 * HOUR,
    'MST': -7 * HOUR,
    'MT': -7 * HOUR,
    'MUT': 4 * HOUR,
    'MVT': 5 * HOUR,
    'MYT': 8 * HOUR,
    'N': -1 * HOUR,
    'NCT': 11 * HOUR,  # noqa: WPS432
    'NDT': 2.5 * HOUR,  # noqa: WPS432
    'NFT': 11 * HOUR,  # noqa: WPS432
    'NOVST': 7 * HOUR,
    'NOVT': 7 * HOUR,
    'NPT': 5.5 * HOUR,  # noqa: WPS432
    'NRT': 12 * HOUR,  # noqa: WPS432
    'NST': 3.5 * HOUR,  # noqa: WPS432
    'NUT': -11 * HOUR,  # noqa: WPS432
    'NZDT': 13 * HOUR,  # noqa: WPS432
    'NZST': 12 * HOUR,  # noqa: WPS432
    'O': -2 * HOUR,
    'OMSST': 7 * HOUR,
    'OMST': 6 * HOUR,
    'ORAT': 5 * HOUR,
    'P': -3 * HOUR,
    'PDT': -7 * HOUR,
    'PET': -5 * HOUR,
    'PETST': 12 * HOUR,  # noqa: WPS432
    'PETT': 12 * HOUR,  # noqa: WPS432
    'PGT': 10 * HOUR,
    'PHOT': 13 * HOUR,  # noqa: WPS432
    'PHT': 8 * HOUR,
    'PKT': 5 * HOUR,
    'PMDT': -2 * HOUR,
    'PMST': -3 * HOUR,
    'PONT': 11 * HOUR,  # noqa: WPS432
    'PST': -8 * HOUR,
    'PT': -8 * HOUR,
    'PWT': 9 * HOUR,
    'PYST': -3 * HOUR,
    'PYT': -4 * HOUR,
    'Q': -4 * HOUR,
    'QYZT': 6 * HOUR,
    'R': -5 * HOUR,
    'RET': 4 * HOUR,
    'ROTT': -3 * HOUR,
    'S': -6 * HOUR,
    'SAKT': 11 * HOUR,  # noqa: WPS432
    'SAMT': 4 * HOUR,
    'SAST': 2 * HOUR,
    'SBT': 11 * HOUR,  # noqa: WPS432
    'SCT': 4 * HOUR,
    'SGT': 8 * HOUR,
    'SRET': 11 * HOUR,  # noqa: WPS432
    'SRT': -3 * HOUR,
    'SST': -11 * HOUR,  # noqa: WPS432
    'SYOT': 3 * HOUR,
    'T': -7 * HOUR,
    'TAHT': -10 * HOUR,
    'TFT': 5 * HOUR,
    'TJT': 5 * HOUR,
    'TKT': 13 * HOUR,  # noqa: WPS432
    'TLT': 9 * HOUR,
    'TMT': 5 * HOUR,
    'TOST': 14 * HOUR,  # noqa: WPS432
    'TOT': 13 * HOUR,  # noqa: WPS432
    'TRT': 3 * HOUR,
    'TVT': 12 * HOUR,  # noqa: WPS432
    'U': -8 * HOUR,
    'ULAST': 9 * HOUR,
    'ULAT': 8 * HOUR,
    'UTC': 0,
    'UYST': -2 * HOUR,
    'UYT': -3 * HOUR,
    'UZT': 5 * HOUR,
    'V': -9 * HOUR,
    'VET': -4 * HOUR,
    'VLAST': 11 * HOUR,  # noqa: WPS432
    'VLAT': 10 * HOUR,
    'VOST': 6 * HOUR,
    'VUT': 11 * HOUR,  # noqa: WPS432
    'W': -10 * HOUR,
    'WAKT': 12 * HOUR,  # noqa: WPS432
    'WARST': -3 * HOUR,
    'WAST': 2 * HOUR,
    'WAT': HOUR,
    'WEST': HOUR,
    'WET': 0,
    'WFT': 12 * HOUR,  # noqa: WPS432
    'WGST': -2 * HOUR,
    'WGT': -3 * HOUR,
    'WIB': 7 * HOUR,
    'WIT': 9 * HOUR,
    'WITA': 8 * HOUR,
    'WST': 14 * HOUR,  # noqa: WPS432
    'WT': 0,
    'X': -11 * HOUR,  # noqa: WPS432
    'Y': -12 * HOUR,  # noqa: WPS432
    'YAKST': 10 * HOUR,
    'YAKT': 9 * HOUR,
    'YAPT': 10 * HOUR,
    'YEKST': 6 * HOUR,
    'YEKT': 5 * HOUR,
    'Z': 0,
})


def date_parser(input_date: str) -> str:
    """Help function to parse timezones correctly in strings.

    Arguments:
        input_date {str} -- Input date as string

    Returns:
        {str} -- Date in isoformat
    """
    parsed_date: datetime = parse_date(input_date, tzinfos=TIMEZONES)
    return parsed_date.isoformat()


# Streams metadata
STREAMS: MappingProxyType = MappingProxyType({
    'dispute_transaction_details': {
        'key_properties': 'id',
        'replication_method': 'INCREMENTAL',
        'replication_key': 'id',
        'bookmark': 'start_date',
        'mapping': {
            'id': {
                'map': 'id', 'null': False,
            },
            'Company Account': {
                'map': 'company_account', 'null': False,
            },
            'Merchant Account': {
                'map': 'merchant_account', 'null': False,
            },
            'Psp Reference': {
                'map': 'psp_reference', 'null': True,
            },
            'Merchant Reference': {
                'map': 'merchant_reference', 'null': True,
            },
            'Payment Method': {
                'map': 'payment_method', 'null': True,
            },
            'Record Date': {
                'map': 'record_date', 'type': date_parser, 'null': True,
            },
            'Record Date TimeZone': {
                'map': 'record_date_timezone', 'null': False,
            },
            'Dispute Currency': {
                'map': 'dispute_currency', 'null': False,
            },
            'Dispute Amount': {
                'map': 'dispute_amount', 'type': Decimal, 'null': True,
            },
            'Record Type': {
                'map': 'record_type', 'null': True,
            },
            'Dispute PSP Reference': {
                'map': 'dispute_psp_reference', 'null': True,
            },
            'Dispute Reason': {
                'map': 'dispute_reason', 'null': True,
            },
            'RFI Scheme Code': {
                'map': 'rfi_scheme_code', 'null': True,
            },
            'RFI Reason Code': {
                'map': 'rfi_reason_code', 'null': True,
            },
            'CB Scheme Code': {
                'map': 'cb_scheme_code', 'null': True,
            },
            'CB Reason Code': {
                'map': 'cb_reason_code', 'null': True,
            },
            'NoF Scheme Code': {
                'map': 'nof_scheme_code', 'null': True,
            },
            'NoF Reason Code': {
                'map': 'nof_reason_code', 'null': True,
            },
            'Payment Date': {
                'map': 'payment_date', 'type': date_parser, 'null': True,
            },
            'Payment Date TimeZone': {
                'map': 'payment_date_timezone', 'null': True,
            },
            'Payment Currency': {
                'map': 'payment_currency', 'null': True,
            },
            'Payment Amount': {
                'map': 'payment_amount', 'type': Decimal, 'null': True,
            },
            'Dispute Date': {
                'map': 'dispute_date', 'type': date_parser, 'null': True,
            },
            'Dispute Date TimeZone': {
                'map': 'dispute_date_timezone', 'null': True,
            },
            'Dispute ARN': {
                'map': 'dispute_arn', 'null': True,
            },
            'User Name': {
                'map': 'user_name', 'null': True,
            },
            'Risk Scoring': {
                'map': 'risk_scoring', 'type': int, 'null': True,
            },
            'Shopper Interaction': {
                'map': 'shopper_interaction', 'null': True,
            },
            'Shopper Name': {
                'map': 'shopper_name', 'null': True,
            },
            'Shopper Email': {
                'map': 'shopper_email', 'null': True,
            },
            'Shopper Reference': {
                'map': 'shopper_reference', 'null': True,
            },
            'Shopper PAN': {
                'map': 'shopper_pan', 'null': True,
            },
            'Iban': {
                'map': 'iban', 'null': True,
            },
            'Bic': {
                'map': 'bic', 'null': True,
            },
            'Shopper IP': {
                'map': 'shopper_ip', 'null': True,
            },
            'Shopper Country': {
                'map': 'shopper_country', 'null': True,
            },
            'Issuer Country': {
                'map': 'issuer_country', 'null': True,
            },
            'Issuer Id': {
                'map': 'issuer_id', 'null': True,
            },
            '3D Directory Response': {
                'map': '3d_directory_response', 'null': True,
            },
            '3D Authentication Response': {
                'map': '3d_authentication_response', 'null': True,
            },
            'CVC2 Response': {
                'map': 'cvc2_response', 'type': int, 'null': True,
            },
            'AVS Response': {
                'map': 'avs_response', 'type': int, 'null': True,
            },
            'Dispute Auto Defended': {
                'map': 'dispute_auto_defended', 'type': bool, 'null': True,
            },
            'Dispute End Date': {
                'map': 'dispute_end_date', 'type': date_parser, 'null': True,
            },
            'Dispute End Date TimeZone': {
                'map': 'dispute_end_date_timezone', 'null': True,
            },
        },
    },
    'payment_accounting': {
        'key_properties': 'id',
        'replication_method': 'INCREMENTAL',
        'replication_key': 'id',
        'bookmark': 'start_date',
        'mapping': {
            'id': {
                'map': 'id', 'null': False,
            },
            'Company Account': {
                'map': 'company_account', 'null': False,
            },
            'Merchant Account': {
                'map': 'merchant_account', 'null': False,
            },
            'Psp Reference': {
                'map': 'psp_reference', 'null': True,
            },
            'Merchant Reference': {
                'map': 'merchant_reference', 'null': True,
            },
            'Payment Method': {
                'map': 'payment_method', 'null': True,
            },
            'Booking Date': {
                'map': 'booking_date', 'type': date_parser, 'null': True,
            },
            'TimeZone': {
                'map': 'timezone', 'null': False,
            },
            'Main Currency': {
                'map': 'main_currency', 'null': True,
            },
            'Main Amount': {
                'map': 'main_amount', 'type': Decimal, 'null': True,
            },
            'Record Type': {
                'map': 'record_type', 'null': True,
            },
            'Payment Currency': {
                'map': 'payment_currency', 'null': True,
            },
            'Received (PC)': {
                'map': 'received', 'type': Decimal, 'null': True,
            },
            'Authorised (PC)': {
                'map': 'authorised', 'type': Decimal, 'null': True,
            },
            'Captured (PC)': {
                'map': 'captured', 'type': Decimal, 'null': True,
            },
            'Settlement Currency': {
                'map': 'settlement_currency', 'null': True,
            },
            'Payable (SC)': {
                'map': 'payable', 'type': Decimal, 'null': True,
            },
            'Commission (SC)': {
                'map': 'commission', 'type': Decimal, 'null': True,
            },
            'Markup (SC)': {
                'map': 'markup', 'type': Decimal, 'null': True,
            },
            'Scheme Fees (SC)': {
                'map': 'scheme_fees', 'type': Decimal, 'null': True,
            },
            'Interchange (SC)': {
                'map': 'interchange', 'type': Decimal, 'null': True,
            },
            'Processing Fee Currency': {
                'map': 'processing_fee_currency', 'null': True,
            },
            'Processing Fee (FC)': {
                'map': 'processing_fee', 'type': Decimal, 'null': True,
            },
            'User Name': {
                'map': 'user_name', 'null': True,
            },
            'Payment Method Variant': {
                'map': 'payment_method_variant', 'null': True,
            },
            'Modification Merchant Reference': {
                'map': 'modification_merchant_reference', 'null': True,
            },
            'Network Token Used': {
                'map': 'network_token_used', 'type': bool, 'null': True,
            },
            'Network Token Available': {
                'map': 'network_token_available', 'type': bool, 'null': True,
            },
        },
    },
    'settlement_details': {
        'key_properties': 'id',
        'replication_method': 'INCREMENTAL',
        'replication_key': 'id',
        'bookmark': 'batch_number',
        'mapping': {
            'id': {
                'map': 'id', 'null': False,
            },
            'Company Account': {
                'map': 'company_account', 'null': False,
            },
            'Merchant Account': {
                'map': 'merchant_account', 'null': False,
            },
            'Psp Reference': {
                'map': 'psp_reference', 'null': True,
            },
            'Merchant Reference': {
                'map': 'merchant_reference', 'null': True,
            },
            'Payment Method': {
                'map': 'payment_method', 'null': True,
            },
            'Creation Date': {
                'map': 'creation_date', 'type': date_parser, 'null': True,
            },
            'TimeZone': {
                'map': 'timezone', 'null': False,
            },
            'Type': {
                'map': 'type', 'null': False,
            },
            'Modification Reference': {
                'map': 'modification_reference', 'null': True,
            },
            'Gross Currency': {
                'map': 'gross_currency', 'null': True,
            },
            'Gross Debit (GC)': {
                'map': 'gross_debit', 'type': Decimal, 'null': True,
            },
            'Gross Credit (GC)': {
                'map': 'gross_credit', 'type': Decimal, 'null': True,
            },
            'Exchange Rate': {
                'map': 'exchange_rate', 'type': Decimal, 'null': True,
            },
            'Net Currency': {
                'map': 'net_currency', 'null': True,
            },
            'Net Debit (NC)': {
                'map': 'net_debit', 'type': Decimal, 'null': True,
            },
            'Net Credit (NC)': {
                'map': 'net_credit', 'type': Decimal, 'null': True,
            },
            'Commission (NC)': {
                'map': 'commission', 'type': Decimal, 'null': True,
            },
            'Markup (NC)': {
                'map': 'markup', 'type': Decimal, 'null': True,
            },
            'Scheme Fees (NC)': {
                'map': 'scheme_fees', 'type': Decimal, 'null': True,
            },
            'Interchange (NC)': {
                'map': 'interchange', 'type': Decimal, 'null': True,
            },
            'Payment Method Variant': {
                'map': 'payment_method_variant', 'null': True,
            },
            'Batch Number': {
                'map': 'batch_number', 'type': int, 'null': True,
            },
            'Modification Merchant Reference': {
                'map': 'modification_merchant_reference', 'null': True,
            },
        },
    },
})
