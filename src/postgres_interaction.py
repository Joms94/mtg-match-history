"""Interact with the Postgres instance on
Supabase. Does things like deleting and
inserting into staging tables, creating
objects or running stored procedures."""

from supabase import create_client, Client, PostgrestAPIResponse
from supabase.lib.client_options import SyncClientOptions


class PostgresDB:
    """Handles authentication and database operations
    against a Supabase managed Postgres instance.

    url: A special project URL provided with each
    Supabase project. Always follows the pattern:
    https://<project_ref>.supabase.co/rest/v1.

    key: API key. This can either be a limited key
    or one associated with a highly-privileged
    service account. Dealer's choice.

    Note: I spent a bit of time hammering my head
    against accessing my schema. You need to go
    into the your project settings -> API configuration
    -> scroll down to 'Exposed schemas' and punch
    in your custom schema for it to be accessible
    via the API, even if you have a full-access
    service account doing the talking."""

    def __init__(self, url: str, key: str) -> None:
        self.client: Client = create_client(
            url,
            key,
            # Make sure you're OK with 'anon' authorisation before using this.
            options=SyncClientOptions(schema="mtg", headers={"Authorization": "anon"}),
        )
        self.staging_tname: str = "fact_staging_matches"

    def delete_from_table(self) -> PostgrestAPIResponse:
        """Delete all table contents. Does not
        supply any filter constraints.

        Used primarily to clear the match staging
        table to begin a new insert."""
        return (
            self.client.table(self.staging_tname)
            .delete()
            .eq("staging_matches_id", 1)
            .execute()
        )

    def insert_into_table(self, data: list[dict[str, str]]) -> PostgrestAPIResponse:
        """Insert data into a Postgres table.
        Currently only used to populate the staging
        table.

        data: Every element in this list represents
        a dictionary consisting of column: value
        pairs. E.g., {'id': '1', 'date': '2024-11-25'}.
        Each dictionary is a row."""
        return self.client.table(self.staging_tname).insert(data).execute()

    def _run_sproc(self, sproc_name: str):
        """Call a stored procedure that currently exists
        in the database.

        Primarily used to drop and re-create all the tables
        via a stored procedure defined within 'db_init.sql'.
        Not terribly efficient to drop the whole structure
        on every insert, but I see no reason to optimise
        given this'll run once a week, clocking in less than
        2k rows per insertion. If it becomes an issue, I'll
        write an upsert procedure."""
        return self.client.rpc(fn=sproc_name).execute()

    def reinitialise_tables(self):
        """Drop and re-create all tables."""
        return self._run_sproc("reinitialise_tables")
