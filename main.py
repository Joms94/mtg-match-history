"""Main file for launching the dashboard."""


import os
import ast

from dotenv import load_dotenv

from src.gsheets_interaction import GoogleSheet
from src.data_cleaning import reformat_api_values_for_postgres
from src.postgres_interaction import PostgresDB


def init() -> dict:
    """Get environment variables. These are primarily
    used to configure APIs."""
    load_dotenv()
    return {
        # Google Sheets.
        "GSHEET_ID": os.getenv("GSHEET_ID"),
        "GOOGLE_CREDS_FPATH": os.getenv("GOOGLE_CREDS_FPATH"),
        "RANGE_NAME": os.getenv("RANGE_NAME"),
        "SCOPES": ast.literal_eval(os.getenv("SCOPES")),
        # Cloud Postgres instance.
        "SUPABASE_URL": os.getenv("SUPABASE_URL"),
        "SUPABASE_KEY": os.getenv("SUPABASE_KEY")
    }


def main():
    """Get result from Google API."""
    config = init()
    # sheet = GoogleSheet(config["GOOGLE_CREDS_FPATH"], config["SCOPES"])
    # data = sheet.get_data(config["GSHEET_ID"], config["RANGE_NAME"])
    # cleaned_data = reformat_api_values_for_postgres(data["values"])
    with open("gsheet_output.txt", mode="r", encoding="utf-8") as mock_data:
        cleaned_data = ast.literal_eval(mock_data.read())
    db = PostgresDB(url=config["SUPABASE_URL"], key=config["SUPABASE_KEY"])
    db.insert_into_table(data=cleaned_data)
    # print(db.reinitialise_tables())


if __name__ == "__main__":
    main()
