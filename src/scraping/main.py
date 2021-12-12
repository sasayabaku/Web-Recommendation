import re
import requests
from bs4 import BeautifulSoup
from icecream import ic

class BookmarkAnalyzer(object):

    def __init__(self) -> None:
        super().__init__()

        self.soup = None
        self.title = None
        self.url = None

    def _get_data(self, url):
        _response = requests.get(url)
        self.soup = BeautifulSoup(_response.text, 'html.parser')

        self.title = self.soup.find('title').text.replace('\u3000', '')

        _text = self.soup.get_text()
        _lines = [line.strip() for line in _text.splitlines()]
        _texts_p = [ t.replace('\n', '') for t in _lines if re.match('\S', t) ]
        _texts_p = [ t.replace('\u3300', '') for t in _texts_p ]
        _texts_p = [ t.replace('\u3000', '') for t in _texts_p ]

        self.texts_p = _texts_p
        

    def _check_data(self, url):
        self._get_data(url)

        ic(self.texts_p)
        ic(self.title)


if __name__ == '__main__':

    url = "https://goodpatch.com/blog/recommend-ux-design-books"

    obj = BookmarkAnalyzer()
    obj._check_data(url)
