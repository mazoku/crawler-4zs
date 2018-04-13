from urllib.request import urlopen
from bs4 import BeautifulSoup
from News import News
import datetime


class Scrapper:

    def __init__(self, base_url, url_class, url_school):
        self.base_url = base_url
        self.url_class = url_class
        self.url_school = url_school

    def scrap_class(self):
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
            except:
                href = None

            # date
            try:
                date = [d for d in new.find_all('p') if d.has_attr('class') and 'datum' in d.attrs['class']][0].text
                date = datetime.datetime.strptime(date, '%d. %m. %Y')
            except:
                date = None

            # message
            try:
                msgs = [d.text for d in new.find_all('p') if len(d.attrs) == 0]
                msg = '\n'.join(msgs)
            except:
                msg = None

            news = News(date, msg, href)
            news_list.append(News)
            print(news)

    def run(self):
        self.scrap_class()




# --------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    base_url = 'https://zs4.plzen.eu'
    url_class_news = 'https://zs4.plzen.eu/stranky-trid-1/1-b/aktuality/'
    url_school_news = 'https://zs4.plzen.eu/nase-skola/aktuality-18/'

    scrapper = Scrapper(base_url, url_class_news, url_school_news)
    scrapper.run()