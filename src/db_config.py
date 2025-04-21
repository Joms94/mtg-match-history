"""Configures the database that will serve
the application and runs operations
against it."""

import sys
import io
from dataclasses import dataclass
from typing import Literal

import duckdb


@dataclass
class Table:
    """Represents schema underlying a database table,
    such as name, columns and data types. Used in
    comparisons against actual corresponding database
    tables to facilitate type conversion, table
    definitions and modifications. Think of this
    as a simple ORM.

    name: Name of the table in the specified database.

    cols_and_dtypes: A dictionary of
    {column name: datatype expressed as string} pairs
    to be used in data type coercion. If a column doesn't
    exist, it's skipped. Uses the Python -> DuckDB object
    conversion specified here:
    https://duckdb.org/docs/stable/clients/python/conversion"""

    name: str
    cols_and_dtypes: dict[str, Literal["INT", "DATE", "VARCHAR", "DOUBLE", "BIT"]]


class Database:
    """Handles DuckDB database connections and operations."""

    def __init__(self, db_name: str) -> None:
        sys.stdout = io.TextIOWrapper(
            sys.stdout.buffer, encoding="utf-8"
        )  # Prevents UnicodeEncodeError in the event utf-8 not in use.
        self.db_name = db_name
        self.con = duckdb.connect(db_name)

    def init_table(self, table: Table, json_fpath: str) -> None:
        """Create a table based on the contents of a json file.
        If a table by the name you've specified exists, drop
        that cheeky bugger, make a new one, then insert into it.

        table: Object containing table information. This method
        only cares about the table name, which is used both
        to create or drop the table, and define the ID column
        name.

        json_fpath: Path to json from which you'll pull data.
        Test json files have normally been unorthodox (read:
        not quite json) in that they've been structured like
        a Python list of dictionaries, with each dictionary
        representing a row of {column header: value} pairs."""
        self.con.sql(
            f"""CREATE OR REPLACE TABLE {table.name} AS
                    SELECT
                        ROW_NUMBER() OVER () AS {table.name}_id,
                        *,
                        current_date AS last_modified_date
                    FROM read_json_auto({json_fpath});"""
        )

    def coerce_dtypes(self, table: Table) -> None:
        """Coerce various columns in a DuckDB table to the
        types you'd like them to be.

        table: Table whose dtypes in the database will be
        coerced to those in this object."""
        cols = (
            self.con.sql(f"SELECT column_name FROM (SHOW {table.name})")
            .to_df()
            .loc[:, "column_name"]
            .to_list()
        )
        self.con.sql(
            "\n".join(
                [
                    f"ALTER TABLE {table.name} ALTER {col_name} TYPE {dtype};"
                    for col_name, dtype in table.cols_and_dtypes.items()
                    if col_name in cols
                ]
            )
        )

    def select_table(self, table: Table) -> None:
        """Display the truncated contents of a table.

        name: Name of table to view."""
        self.con.sql(f"SELECT * FROM {table.name};").show()


if __name__ == "__main__":
    staging = Table(
        name="staging_matches", cols_and_dtypes={"match_date": "DATE", "pod_id": "INT"}
    )
    db = Database("mtg_stats.db")
    db.init_table(table=staging, json_fpath="gsheet_values.json")
    db.coerce_dtypes(table=staging)
    db.select_table(table=staging)
