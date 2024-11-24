"""Fixtures for use throughout the test suite.
Handles setup/ teardown. These are accessible
by pytest in all modules with the 'test_'
prefix, even when not explicitly imported."""


import pytest


@pytest.fixture
def api_values() -> list[list[str]]:
    """Returns test values in the style of
    Google Cloud's API when the 'values'
    key is accessed.

    The first row represents headers.
    All subsequent rows represent values,
    with each list being a row, and each
    element being a cell in that row.
    
    Useful for testing transformations
    performed on Google Sheets data
    directly after it has been accessed."""
    return [
        ["header A1", "header B1", "header C1"],
        ["value A2", "value B2", "value C2"],
        ["value A3", "value B3", "value C3"]
    ]
