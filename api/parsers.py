from html.parser import HTMLParser


class HackerNewsHtmlParser(HTMLParser):
    def error(self, message):
        raise HackerNewsHtmlParserException(message)

    def __init__(self, *, convert_charrefs=True):
        super().__init__(convert_charrefs=convert_charrefs)
        self._in_table = False
        self._in_athing = False
        self._in_title = False
        self._last_url = None
        self.pairs = []

    def handle_starttag(self, tag, attrs):
        if self._in_title and 'a' == tag and ('class', 'storylink') in attrs:
            for attr, val in attrs:
                if attr == 'href':
                    self._last_url = val.strip()
                    break
        elif self._in_athing and 'td' == tag and ('class', 'title') in attrs:
            self._in_title = True
        elif self._in_table and 'tr' == tag and ('class', 'athing') in attrs:
            self._in_athing = True
        elif not self._in_table and 'table' == tag and ('class', 'itemlist') in attrs:
            self._in_table = True

    def handle_endtag(self, tag):
        if self._last_url is not None and 'a' == tag:
            self._last_url = None
        if self._in_title and 'td' == tag:
            self._in_title = False
        if self._in_athing and 'tr' == tag:
            self._in_athing = False
        if self._in_table and 'table' == tag:
            self._in_table = False

    def handle_data(self, data):
        if self._last_url is not None:
            self.pairs.append((self._last_url, data.strip()))
            self._last_url = None


class HackerNewsHtmlParserException(Exception):
    pass
