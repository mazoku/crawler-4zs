import gspread
from oauth2client.service_account import ServiceAccountCredentials


class Spreadsheetator:

    def __init__(self):
        self.sheet = None
        self.trida_ws = None

        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']

        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            '/home/tomas/Dropbox/Documents/keys/Scrapper-4ZS-7ef5a34bb156.json', scope)

        gc = gspread.authorize(credentials)

        # get spreadsheet
        self.sheet = gc.open("Scrapper-4ZS")
        # get worksheets
        self.trida_ws = self.sheet.worksheet('trida')

    def read_all(self):
        # list data in first column
        # values_list = self.trida_ws.col_values(1)
        # print(values_list)

        data = self.trida_ws.get_all_values()
        print(data)


# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    stator = Spreadsheetator()
    stator.read_all()