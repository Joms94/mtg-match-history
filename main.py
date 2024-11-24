"""Main file for launching the dashboard."""


import os
import ast

from dotenv import load_dotenv

from src.gsheets_interaction import GoogleSheet


def init() -> dict:
    """Get environment variables. These are primarily
    used to configure and use the Google Cloud API.
    See gsheets_interaction.py for details."""
    load_dotenv()
    return {
        "GSHEET_ID": os.getenv("GSHEET_ID"),
        "CREDS_FPATH": os.getenv("CREDS_FPATH"),
        "RANGE_NAME": os.getenv("RANGE_NAME"),
        "SCOPES": ast.literal_eval(os.getenv("SCOPES"))
    }


def main():
    """Get result from Google API."""
    config = init()
    sheet = GoogleSheet(config["CREDS_FPATH"], config["SCOPES"])
    print(sheet.get_data(config["GSHEET_ID"], config["RANGE_NAME"]))


if __name__ == "__main__":
    main()
