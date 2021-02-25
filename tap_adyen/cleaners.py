"""Cleaner functions."""
# -*- coding: utf-8 -*-

from datetime import date
from types import MappingProxyType
from typing import Any, Optional

from tap_adyen.streams import STREAMS


class ConvertionError(ValueError):
    """Failed to convert value."""


def to_type_or_null(
    input_value: Any,
    data_type: Optional[Any] = None,
    nullable: bool = True,
) -> Optional[Any]:
    """Convert the input_value to the data_type.

    The input_value can be anything. This function attempts to convert the
    input_value to the data_type. The data_type can be a data type such as str,
    int or Decimal or it can be a function. If nullable is True, the value is
    converted to None in cases where the input_value == None. For example:
    a '' == None, {} == None and [] == None.

    Arguments:
        input_value {Any} -- Input value

    Keyword Arguments:
        data_type {Optional[Any]} -- Data type to convert to (default: {None})
        nullable {bool} -- Whether to convert empty to None (default: {True})

    Returns:
        Optional[Any] -- The converted value
    """
    # If the input_value is not equal to None and a data_type input exists
    if input_value and data_type:
        # Convert the input value to the data_type
        try:
            return data_type(input_value)
        except ValueError as err:
            raise ConvertionError(
                f'Could not convert {input_value} to {data_type}: {err}',
            )

    # If the input_value is equal to None and Nullable is True
    elif not input_value and nullable:
        # Convert '', {}, [] to None
        return None

    # If the input_value is equal to None, but nullable is False
    # Return the original value
    return input_value


def clean_row(row: dict, mapping: dict) -> dict:
    """Clean the row according to the mapping.

    The mapping is a dictionary with optional keys:
    - map: The name of the new key/column
    - type: A data type or function to apply to the value of the key
    - nullable: Whether to convert empty values, such as '', {} or [] to None

    Arguments:
        row {dict} -- Input row
        mapping {dict} -- Input mapping

    Returns:
        dict -- Cleaned row
    """
    cleaned: dict = {}

    key: str
    key_mapping: dict

    # For every key and value in the mapping
    for key, key_mapping in mapping.items():

        # Retrieve the new mapping or use the original
        new_mapping: str = key_mapping.get('map') or key

        # Convert the value
        cleaned[new_mapping] = to_type_or_null(
            row[key],
            key_mapping.get('type'),
            key_mapping.get('null', True),
        )

    return cleaned


def clean_payment_accounting(
    row: dict,
    file_date: date,
    row_number: int,
) -> dict:
    """Clean payment accounting.

    Arguments:
        row {dict} -- Input row
        file_date {date} -- File date, used to construct primary key
        row_number {int} -- Row number, used to construct primary key

    Returns:
        dict -- Cleaned row
    """
    # Get the mapping from the STREAMS
    mapping: Optional[dict] = STREAMS['payment_accounting'].get('mapping')

    # Create primary key
    date_string: str = '{date:%Y%m%d}'.format(date=file_date)  # noqa: WPS323
    number: str = str(row_number).rjust(10, '0')
    row['id'] = int(date_string + number)

    # Add timezone to the date, so that the datetime parser includes it
    row['Booking Date'] = '{booking_date} {timezone}'.format(
        booking_date=row.get('Booking Date', ''),
        timezone=row.get('TimeZone', ''),
    )

    # If a mapping has been defined in STREAMS, apply it
    if mapping:
        return clean_row(row, mapping)

    # Else return the original row
    return row


def clean_settlement_details(row: dict, row_number: int) -> dict:
    """Clean settlement details.

    Arguments:
        row {dict} -- Input row
        row_number {int} -- Row number, used to construct primary key

    Returns:
        dict -- Cleaned row
    """
    # Get the mapping from the STREAMS
    mapping: Optional[dict] = STREAMS['settlement_details'].get('mapping')

    # Create primary key
    number: str = str(row_number).rjust(10, '0')
    row['id'] = int(row['Batch Number'] + number)

    # Add timezone to the date, so that the datetime parser includes it
    row['Creation Date'] = '{creation_date} {timezone}'.format(
        creation_date=row.get('Creation Date', ''),
        timezone=row.get('TimeZone', ''),
    )

    # If a mapping has been defined in STREAMS, apply it
    if mapping:
        return clean_row(row, mapping)

    # Else return the original row
    return row


# Collect all cleaners
CLEANERS: MappingProxyType = MappingProxyType({
    'settlement_details': clean_settlement_details,
})
