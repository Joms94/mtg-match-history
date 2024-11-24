"""Module responsible for cleaning data
from Google Sheets and databases."""

from collections import defaultdict


def reformat_api_values(data: list[list[str]]) -> dict[str, list[str]]:
    """Designed to clean data returned by the
    Google Cloud API. The 'values' portion
    of the dictionary typically returned is
    structured as a list of lists, with the
    first list being the header row.

    Returns a dictionary of column headers as
    keys and lists as values (rows), with each
    element representing a cell in that row.

    Purpose is to make it easier to work with
    this data in future. E.g., passing it to
    DataFrames."""
    cleaned_data = defaultdict(list)
    for col_ind, col in enumerate(data[0]):
        cleaned_data[col] += [row[col_ind] for row in data[1:]]
    return cleaned_data
