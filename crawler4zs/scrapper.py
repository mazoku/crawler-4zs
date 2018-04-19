#!/home/tomas/projects/crawler-4zs/venv/bin/python
from urllib.request import urlopen
from bs4 import BeautifulSoup
from news import News
import datetime
from spreadsheetator import Spreadsheetator


class Scrapper:

    def __init__(self, base_url, url_class, url_school):
        print('\n\n---------------------------------------------------------------------------------------')
        print('Runtime: {}'.format(datetime.datetime.now().strftime("%-d.%-m.%Y %H:%M:%S")))

        self.base_url = base_url
        self.url_class = url_class
        self.url_school = url_school
        print('connecting to spreadsheet ...')
        self.sheetator = Spreadsheetator()

    def scrap_class(self, verbose=False):
        html_page = urlopen(self.url_class)
        html_text = html_page.read().decode('utf-8')
        my_soup = BeautifulSoup(html_text, 'html.parser')
        # divs = my_soup.find_all('div')
        news = [div for div in my_soup.find_all('div') if div.has_attr('class') and 'aktualita' in div.attrs['class']]

        news_list = []
        for new in news:
            # hyperlink
            try:
                href = self.base_url + new.find_all('a')[0].attrs['href']
                title = new.find_all('a')[0].text
            except:
                href = ''
                title = ''

            # date
            try:
                date = [d for d in new.find_all('p') if d.has_attr('class') and 'datum' in d.attrs['class']][0].text
                # date = datetime.datetime.strptime(date, '%-d. %-m. %-Y')
            except:
                date = ''

            # message
            try:
                msgs = [d.text for d in new.find_all('p') if len(d.attrs) == 0]
                msg = '\n'.join(msgs)
            except:
                msg = ''

            news = News(date, title, href, msg)
            news_list.append(news)

        # print
        if verbose:
            for news in news_list:
                print(news)

        return news_list

    def find_untracked_news(self, tracked_news, class_news):
        # get the last tracked news
        last_tracked = max(tracked_news, key=lambda x: x.date)

        # find untracked news
        untracked_news = [news for news in class_news if news.date >= last_tracked.date and news.title != last_tracked.title]

        return untracked_news


    def sync_class_news(self):
        # scrap all class news
        print('scrapping the url: {} ...'.format(self.url_class))
        class_news = self.scrap_class()

        # read tracked news
        print('reading tracked news from sheet ... ', end='')
        tracked_news = self.sheetator.read_all()
        print('done, found {} news'.format(len(tracked_news)))

        # find all untracked news
        print('finding untracked news ... ', end='')
        untracked_news = self.find_untracked_news(tracked_news, class_news)
        print('done, found {} news'.format(len(untracked_news)))

        # write untracked news into the sheet
        if untracked_news:
            print('writing untracked news ... ', end='')
            self.sheetator.append(untracked_news)
            print('done')
        else:
            print('no untracked news')

        print('all done')

    def run(self):
        # update / sync class news
        self.sync_class_news()

# --------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    base_url = 'https://zs4.plzen.eu'
    url_class_news = 'https://zs4.plzen.eu/stranky-trid-1/1-b/aktuality/'
    url_school_news = 'https://zs4.plzen.eu/nase-skola/aktuality-18/'

    scrapper = Scrapper(base_url, url_class_news, url_school_news)
    scrapper.run()