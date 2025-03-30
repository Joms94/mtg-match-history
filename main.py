"""Main file for launching the dashboard."""


import os
import ast
import json

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
        GSHEET: os.getenv(GSHEET),
        GCREDS: os.getenv(GCREDS),
        GRANGE: os.getenv(GRANGE),
        SCOPES: ast.literal_eval(os.getenv(SCOPES))
    }


def main():
    """Get result from Google API."""
    config = init()
    sheet = GoogleSheet(config[GCREDS], config[SCOPES])
    data = sheet.get_data(config[GSHEET], config[GRANGE])
    with open("gsheet_output.json", mode="w+", encoding="utf-8") as output_file:
        json.dump(data, output_file)


if __name__ == "__main__":
    main()
