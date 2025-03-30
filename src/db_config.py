"""Configures the database that will serve
the application and runs operations
against it."""


import sys
import io
import json

import duckdb


def init_db(json_fpath: str, db_name: str = "mtg_stats.db") -> None:
    """Initialise a persistent storage variant
    of a DuckDB database by loading staging data
    into it.

    data: A dictionary containing column headers
    as the keys, and lists of strings as values.
    
    db_name: Name of the on-disk database."""
    with duckdb.connect(db_name) as con:
        con.sql(f"""CREATE OR REPLACE TABLE staging_fact AS
                        SELECT * FROM read_json_auto({json_fpath});""")


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8') # Prevents UnicodeEncodeError in the event utf-8 not in use.
    # with open("gsheet_values.json", mode="rb") as json_binary:
    #     data = json.load(json_binary)
    init_db(json_fpath="gsheet_values.json")
    with duckdb.connect("mtg_stats.db") as con:
        con.sql("SELECT * FROM staging_fact;").show()
