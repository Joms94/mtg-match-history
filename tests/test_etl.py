"""Tests extract, transform and load (ETL)
functionality. Includes transformations for
both input data from Google Sheets and match
data already in the database."""


from src.data_cleaning import reformat_api_values


def test_reformat_values_dict(api_values):
    """Figure out if we're correctly converting
    the list of lists supplied by the Google
    Cloud API into a dictionary consisting of
    column headers as keys and rows as values."""
    keys_to_check = api_values[0]
    data = reformat_api_values(api_values)
    assert all(key in data.keys() for key in keys_to_check)
    assert all(len(data[key]) == 2 for key in keys_to_check)
