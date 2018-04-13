
class News:

    def __init__(self, date, msg, href):
        self.date = date
        self.msg = msg
        self.href = href

    def __str__(self):
        return '{}: {}, href= {}'.format(self.date.strftime('%-d. %-m. %Y'), self.msg, self.href)