from html.parser import HTMLParser


class HackerNewsHtmlParser(HTMLParser):
    def error(self, message):
        raise HackerNewsHtmlParserException(message)

    def __init__(self, *, convert_charrefs=True):
        super().__init__(convert_charrefs=convert_charrefs)
        self.in_table = False
        self.in_athing = False
        self.in_title = False
        self.last_url = None
        self.pairs = []

    def handle_starttag(self, tag, attrs):
        if self.in_title and 'a' == tag and ('class', 'storylink') in attrs:
            for attr, val in attrs:
                if attr == 'href':
                    self.last_url = val
                    break
        elif self.in_athing and 'td' == tag and ('class', 'title') in attrs:
            self.in_title = True
        elif self.in_table and 'tr' == tag and ('class', 'athing') in attrs:
            self.in_athing = True
        elif not self.in_table and 'table' == tag and ('class', 'itemlist') in attrs:
            self.in_table = True

    def handle_endtag(self, tag):
        if self.last_url is not None and 'a' == tag:
            self.last_url = None
        if self.in_title and 'td' == tag:
            self.in_title = False
        if self.in_athing and 'tr' == tag:
            self.in_title = False
        if self.in_table and 'table' == tag:
            self.in_title = False

    def handle_data(self, data):
        if self.last_url is not None:
            self.pairs.append((self.last_url, data.strip()))


class HackerNewsHtmlParserException(Exception):
    pass
