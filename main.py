"""Main file for loading data from source, staging
it in the database, then building visualisations."""

import os
import ast

from dotenv import load_dotenv

from src.gsheets_interaction import GoogleSheet


# .env file parameter names. Used for authentication.
GSHEET = "GSHEET_ID"
GCREDS = "GOOGLE_CREDS_FPATH"
GRANGE = "RANGE_NAME"
SCOPES = "SCOPES"


def init() -> dict:
    """Get environment variables. These are primarily
    used to configure APIs."""
    load_dotenv()
    return {
        # Google Sheets.
        GSHEET: os.getenv(
            GSHEET
        ),  # The jumbled characters in the URL after /spreadsheets/d/.
        GCREDS: os.getenv(GCREDS),  # Path to your service-account-keys.json.
        GRANGE: os.getenv(GRANGE),  # Range to pull from. E.g., "A2:B10".
        SCOPES: ast.literal_eval(
            os.getenv(SCOPES)
        ),  # E.g., https://www.googleapis.com/auth/spreadsheets.readonly.
    }


def main():
    """Get result from Google API."""
    config = init()
    sheet = GoogleSheet(creds_fpath=config[GCREDS], scopes=config[SCOPES])
    sheet.get_data(gsheet_id=config[GSHEET], data_range=config[GRANGE])


if __name__ == "__main__":
    main()
