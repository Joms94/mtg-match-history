"""Configures the database that will serve
the application and runs operations
against it."""


import sys
import io

import duckdb

from data_cleaning import get_api_values, load_json_values


def init_db(data: dict[str, list[str]], db_name: str = "mtg_stats.db") -> None:
    """Initialise a persistent storage variant
    of a DuckDB database by loading staging data
    into it.

    data: A dictionary containing column headers
    as the keys, and lists of strings as values.
    
    db_name: Name of the on-disk database."""
    with duckdb.connect(db_name) as con:
        con.sql("""CREATE OR REPLACE TABLE staging_fact AS
                        SELECT * FROM data;""")


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8') # Prevents UnicodeEncodeError in the event utf-8 not in use.
    json_vals = load_json_values()
    data = get_api_values(json_vals)
    init_db(data=data)
    with duckdb.connect("mtg_stats.db") as con:
        con.sql("SELECT * FROM staging_fact;").show()
