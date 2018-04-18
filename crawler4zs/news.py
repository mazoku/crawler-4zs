import datetime

class News:

    def __init__(self, date, title, href, msg):
        self.date = datetime.datetime.strptime(date, '%d. %m. %Y') # date
        self.title = title
        self.href = href
        self.msg = msg

        # replace hard spaces
        self.msg = self.msg.replace('\xa0', ' ')

    def print_format(self):
        return([self.date.strftime('%-d. %-m. %Y'), self.title, self.href, self.msg])
        # return([self.date, self.title, self.href, self.msg])

    def __str__(self):
        return '{}: {}, href= {}'.format(self.date.strftime('%-d. %-m. %Y'), self.title, self.href)
        # return '{}: {}, href= {}'.format(self.date, self.title, self.href)

    def __repr__(self):
        return '{}: {}, href= {}'.format(self.date.strftime('%-d. %-m. %Y'), self.title, self.href)