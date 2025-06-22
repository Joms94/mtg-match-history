"""Module responsible for configuring Google Cloud
API connections and pulling sheet data."""

import json

from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials


class GoogleSheet:
    """Authenticates with the Google Cloud API
    and gets the contents of a sheet.

    creds_fpath: a .json supplied in the Google
    Cloud developer portal when you set up a
    service account for your project.

    scopes: OAuth 2 scopes required by Google.
    Even when you're using a service account,
    this still seems necessary. For more info:
    https://developers.google.com/identity/protocols/oauth2/scopes

    gsheet_id: There's a jumble of characters
    in the URL for every GSheet between '/d/'
    and '/edit'. This is your gsheet_id.

    data_range: The name of a range specified
    in the same manner as you would within
    a typical Sheets formula. E.g., if you
    were trying to access the first column
    and first 10 rows of a sheet, this might
    be Sheet1!A1:A10, substituting 'Sheet1'
    with your actual sheet name."""

    def __init__(
        self, creds_fpath: str, scopes: list[str], gsheet_id: str, data_range: str
    ) -> None:
        self.creds = Credentials.from_service_account_file(creds_fpath, scopes=scopes)
        self.gsheet_id = gsheet_id
        self.data_range = data_range
        self.api_data = {"range": None, "majorDimension": None, "values": [[None]]}

    def query_api(self) -> None:
        """Get data and metadata from the Google
        API based on various parameters."""
        with build("sheets", "v4", credentials=self.creds) as service:
            self.api_data = (
                service.spreadsheets()
                .values()
                .get(spreadsheetId=self.gsheet_id, range=self.data_range)
                .execute()
            )

    def _clean_api_values(self) -> None:
        """Designed to clean data returned by the
        Google Cloud API. The 'values' portion
        of the dictionary returned is
        structured as a list of lists, with the
        first list being the header row.

        Overwrites `api_data` with a list
        of dictionaries. Each dictionary is
        a {column header:value} pair for every
        column in the row.

        Purpose is to trivialise an otherwise-
        difficult cleaning operation were I
        to load the json raw into a staging
        table and transform using pure SQL."""
        data = self.api_data["values"]
        row_data = []
        headers = [data[0]]*(data_len:=len(data[1:])) # List of headers for each row.
        for row in range(data_len):
            row_data.append(dict(zip(headers[row], data[1:][row])))
        self.api_data = row_data

    def write_api_values(self, output_fname: str = "gsheet_values.json") -> None:
        """Write Google API data to a .json file for
        use in later database operations or diagnostics."""
        with open(output_fname, mode="w+", encoding="utf-8") as output_file:
            json.dump(self.api_data, output_file)

    def get_data(
        self, output_fname: str = "gsheet_values.json", clean: bool = True
    ) -> None:
        """Convenience method responsible for
        hitting the API, reading all data to
        a dictionary, cleaning the values so
        they're easier to parse in future
        database operations, then write
        to JSON.

        output_fname: Name of json file to
        write to.

        clean: Whether to clean the API data
        prior to writing it. Default True.
        If False, provide just as papa Google
        serves it up."""
        self.query_api()
        if clean:
            self._clean_api_values()
        self.write_api_values(output_fname=output_fname)
