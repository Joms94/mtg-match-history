"""Main file for loading data from source, staging
it in the database, then building visualisations."""

import os
import ast

from dotenv import load_dotenv

from src.gsheets_interaction import GoogleSheet
from src.db_config import Table, Database


# .env file parameter names. Used for authentication.
GSHEET = "GSHEET_ID"
GCREDS = "GOOGLE_CREDS_FPATH"
GRANGE = "RANGE_NAME"
SCOPES = "SCOPES"

# Local constants for other uses.
JSON_FNAME = "gsheet_values.json"  # Output filename for Google Sheets data.


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
    """Get result from Google API, then populate DB tables."""

    # Pull data from sheet into JSON.
    config = init()
    sheet = GoogleSheet(
        creds_fpath=config[GCREDS],
        scopes=config[SCOPES],
        gsheet_id=config[GSHEET],
        data_range=config[GRANGE],
    )
    sheet.get_data(output_fname=JSON_FNAME)

    # Pull data from JSON into staging table.
    staging = Table(
        name="staging_matches",
        cols_and_dtypes={
            "player_one_name": "VARCHAR",
            "player_one_commander": "VARCHAR",
            "player_two_name": "VARCHAR",
            "player_two_commander": "VARCHAR",
            "player_three_name": "VARCHAR",
            "player_three_commander": "VARCHAR",
            "player_four_name": "VARCHAR",
            "player_four_commander": "VARCHAR",
            "player_five_name": "VARCHAR",
            "player_five_commander": "VARCHAR",
            "winner_name": "VARCHAR",
            "winner_commander": "VARCHAR",
            "pod_id": "INT",
            (watermark := "match_date"): "DATE"
        },
        watermark_col=watermark, # Used to determine if a record is new or not.
    )
    db = Database("mtg_stats.db")
    db.init_table(table=staging)
    db.upsert_table(table=staging, json_fpath=JSON_FNAME)
    db.select_table(table=staging)

    # Load staging into facts and dimensions.

    # Build visuals.


if __name__ == "__main__":
    main()
