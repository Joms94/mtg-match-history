"""Tests extract, transform and load (ETL)
functionality. Includes transformations for
both input data from Google Sheets and match
data already in the database."""

from src.data_cleaning import (
    reformat_api_values_for_df,
    reformat_api_values_for_postgres,
)


def test_reformat_values_df(google_api_values):
    """Figure out if we're correctly converting
    the list of lists supplied by the Google
    Cloud API into a dictionary consisting of
    column headers as keys and rows as values."""
    keys_to_check = google_api_values[0]
    data = reformat_api_values_for_df(google_api_values)
    assert all(key in data.keys() for key in keys_to_check)
    assert all(len(data[key]) == 2 for key in keys_to_check)


def test_reformat_values_postgres(google_api_values):
    """Test whether the Google Sheets data
    reformatting function correctly converts
    the format to that expected by the
    Supabase API."""
    keys_to_check = google_api_values[0]
    rows = reformat_api_values_for_postgres(google_api_values)
    for row in rows:
        # Check key existence.
        assert all(key in row.keys() for key in keys_to_check)
        # Check for exactly one value per key.
        assert len(row.values()) == len(row.keys())
