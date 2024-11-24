"""Module responsible for configuring Google Cloud
API connections, pulling sheet data, then coercing
it into a more useable format."""


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
    https://developers.google.com/identity/protocols/oauth2/scopes"""
    def __init__(self, creds_fpath: str, scopes: str) -> None:
        self.creds_fpath = creds_fpath
        self.scopes = scopes
        self.creds = Credentials.from_service_account_file(creds_fpath, scopes=scopes)

    def get_data(self, gsheet_id: str, range_name: str) -> dict[str, list[str]]:
        """Extract data from a sheet in your
        Google Sheets workbook..
        
        range_name: The name of a range specified
        in the same manner as you would within
        a typical Sheets formula. E.g., if you
        were trying to access the first column
        and first 10 rows of a sheet, this might
        be Sheet1!A1:A10, substituting 'Sheet1'
        with your actual sheet name.
        
        gsheet_id: There's a jumble of characters
        in the URL for every GSheet between '/d/'
        and '/edit'. This is your gsheet_id."""
        with build('sheets', 'v4', credentials=self.creds) as service:
            return service.spreadsheets().values().get(spreadsheetId=gsheet_id, range=range_name).execute()
