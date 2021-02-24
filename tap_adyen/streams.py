"""Streams metadata."""
# -*- coding: utf-8 -*-
from decimal import Decimal
from types import MappingProxyType

from dateutil.parser import parse as parse_date

# Streams metadata
STREAMS: MappingProxyType = MappingProxyType({
    'settlement_details': {
        'key_properties': 'tbd',
        'replication_method': 'INCREMENTAL',
        'replication_key': 'tbd',
        'bookmark': 'tbd',
        'mapping': {
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
                'map': 'creation_date', 'type': parse_date, 'null': True,
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
                'map': 'gross_currency', 'null': False,
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
                'map': 'net_crebit', 'type': Decimal, 'null': True,
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
