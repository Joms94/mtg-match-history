"""Interact with the Postgres instance on
Supabase. Does things like deleting and
inserting into staging tables, creating
objects or running stored procedures."""

from supabase import create_client, Client, PostgrestAPIResponse


class PostgresDB:
    """Handles authentication and database operations
    against a Supabase managed Postgres instance.

    url: A special project URL provided with each
    Supabase project. Always follows the pattern:
    https://<project_ref>.supabase.co/rest/v1.

    key: API key. This can either be a limited key
    or one associated with a highly-privileged
    service account. Dealer's choice."""

    def __init__(self, url: str, key: str) -> None:
        self.client: Client = create_client(url, key)
        self.staging_tname: str = "postgres.mtg.fact_staging_matches"

    def delete_from_table(self) -> PostgrestAPIResponse:
        """Delete all table contents. Does not
        supply any filter constraints.

        Used primarily to clear the match staging
        table to begin a new insert."""
        return self.client.table(self.staging_tname).delete().execute()

    def insert_into_table(self, data: list[dict[str, str]]) -> PostgrestAPIResponse:
        """Insert data into a Postgres table.
        Currently only used to populate the staging
        table.

        data: Every element in this list represents
        a dictionary consisting of column: value
        pairs. E.g., {'id': '1', 'date': '2024-11-25'}.
        Each dictionary is a row."""
        return self.client.table(self.staging_tname).insert(data).execute()
