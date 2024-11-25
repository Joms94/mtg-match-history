"""Module responsible for cleaning data
from Google Sheets and databases."""


from collections import defaultdict


def reformat_api_values_for_df(data: list[list[str]]) -> dict[str, list[str]]:
    """Designed to clean data returned by the
    Google Cloud API. The 'values' portion
    of the dictionary typically returned is
    structured as a list of lists, with the
    first list being the header row.

    Returns a dictionary of column headers as
    keys and lists as values (rows), with each
    element representing a cell in that row.

    Purpose is to make it easier to load this
    data into DataFrames. May not be necessary
    in future, but I'll likely want to generate
    CSVs and read from them while I test
    and build this thing, which is easy
    from a DataFrame."""
    cleaned_data = defaultdict(list)
    for col_ind, col in enumerate(data[0]): # Iterate over headers.
        cleaned_data[col] += [row[col_ind] for row in data[1:]]
    return cleaned_data


def reformat_api_values_for_postgres(data: list[list[str]]) -> list[dict[str, str]]:
    """Reformats values supplied by Google Cloud
    API for the thin Supabase API layer for
    their Postgres instances.
    
    Used to insert sheet data directly into
    the database rather than dicking around
    with DataFrames, SQLAlchemy and greasy
    monkey-work in general."""
    row_data = []
    headers = [data[0]]*(data_len:=len(data[1:])) # List of headers for each row.
    for row in range(data_len):
        row_data.append(dict(zip(headers[row], data[1:][row])))
    return row_data
