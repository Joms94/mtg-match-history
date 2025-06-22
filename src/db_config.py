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
    https://duckdb.org/docs/stable/clients/python/conversion

    watermark_col: Date column used to distinguish old records
    from new."""

    name: str
    cols_and_dtypes: dict[
        str, Literal["INT", "DATE", "VARCHAR", "DOUBLE", "BIT"]
    ]
    watermark_col: str


class Database:
    """Handles DuckDB database connections and operations.

    Please note: this was written for a local personal project.
    Security liberties have been taken. For instance,
    queries in these methods are not parameterisied properly."""

    def __init__(self, db_name: str) -> None:
        sys.stdout = io.TextIOWrapper(
            sys.stdout.buffer, encoding="utf-8"
        )  # Prevents UnicodeEncodeError in the event utf-8 not in use.
        self.db_name = db_name
        self.con = duckdb.connect(db_name)

    def init_table(self, table: Table, force_drop: bool = False) -> None:
        """Create a table based on the contents of a json file.
        If a table by the name you've specified exists, do nothing.
        Creates sequences to produce auto-incrementing primary keys
        and watermarks.

        table: Object containing table information. Used to create
        the table if it doesn't already exist

        force_drop: Drop the table without question. Used when
        the underlying schema of the source data changes and
        the table needs to reflect that."""
        if force_drop:
            self.con.sql(
                f"""DROP TABLE IF EXISTS {table.name};
                DROP SEQUENCE IF EXISTS id_sequence;"""
            )

        self.con.sql(
            f"""
            CREATE SEQUENCE IF NOT EXISTS id_sequence START 1;

            CREATE TABLE IF NOT EXISTS {table.name} (
                {table.name}_id INT PRIMARY KEY DEFAULT nextval('id_sequence'),
                {",".join((col + " " + dtype) for col, dtype in table.cols_and_dtypes.items())},
                last_modified TIMESTAMP_S DEFAULT current_localtimestamp()
            );
            """
        )

    def upsert_table(self, table: Table, json_fpath: str) -> None:
        """Inserts new records and updates old ones
        in the specified table."""
        self.con.sql(
            f"""
            INSERT OR REPLACE INTO {table.name} (
                {(cols:=",".join(table.cols_and_dtypes.keys()))}
            )
                SELECT {cols}
                FROM read_json_auto({json_fpath})
                WHERE {table.watermark_col} > (
                    SELECT COALESCE(MAX({table.watermark_col}), '1900-01-01') FROM {table.name}
                )
            """
        )

    def select_table(self, table: Table) -> None:
        """Display the truncated contents of a table.

        name: Name of table to view."""
        self.con.sql(f"SELECT * FROM {table.name};").show()
