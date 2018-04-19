import gspread
from oauth2client.service_account import ServiceAccountCredentials
from  news import News


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

    def append(self, data):
        if isinstance(data, list):
            data = sorted(data, key=lambda x: x.date)
            for row in data:
                self.trida_ws.insert_row(row.print_format(), 2, 'USER_ENTERED')
        else:
            self.trida_ws.insert_row(data.print_format(), 2, 'USER_ENTERED')

    def read_all(self, verbose=False):
        data = self.trida_ws.get_all_values()[1:]
        news_list = []
        for row in data:
            news = News(*row)
            news_list.append(news)

        # print
        if verbose:
            for news in news_list:
                print(news)
        return news_list


# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    stator = Spreadsheetator()
    stator.read_all(verbose=True)
    stator.append(['18.4.2018', 'Nadpis - insert test', 'odkaz - insert test', 'obsah - insert test'])
    stator.read_all()