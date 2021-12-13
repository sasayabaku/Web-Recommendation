import re
import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient

from icecream import ic

MONGO_URL = "localhost"
MONGO_PORT = 27017
MONGO_USER = "root"
MONGO_PASS = "root"

class BookmarkAnalyzer(object):

    def __init__(self) -> None:
        super().__init__()

        self.soup = None
        self.title = None
        self.url = None

        self.mongo_client = MongoClient(
            MONGO_URL,
            MONGO_PORT,
            username=MONGO_USER,
            password=MONGO_PASS
        )

        self.mongo_db = self.mongo_client.url_database
        self.mongo_collection = self.mongo_db.url_collection

    def _get_data(self, url):
        _response = requests.get(url)
        self.soup = BeautifulSoup(_response.text, 'html.parser')

        self.title = self.soup.find('title').text.replace('\u3000', '')

        _text = self.soup.get_text()
        _lines = [line.strip() for line in _text.splitlines()]
        _texts_p = [ t.replace('\n', '') for t in _lines if re.match('\S', t) ]
        _texts_p = [ t.replace('\u3300', '') for t in _texts_p ]
        _texts_p = [ t.replace('\u3000', '') for t in _texts_p ]
        _texts_p = [ t.replace('\uf002', '') for t in _texts_p ]

        self.texts_p = _texts_p
        
    def post_url(self, url):

        self._get_data(url)

        post = {
            "url": url,
            "title": self.title,
            "texts": self.texts_p
        }

        self.mongo_collection.update_one(
            {"url": url},
            {"$setOnInsert": post},
            upsert=True
        )

    def _check_mongo(self):
        ic("Mongo DB ====>")
        for doc in self.mongo_collection.find():
            ic(doc['url'])

    def _check_data(self, url):
        self.post_url(url)

        ic(self.texts_p)
        ic(self.title)

        self._check_mongo()

        

if __name__ == '__main__':

    url = "https://ux-jump.com/ux-process"

    obj = BookmarkAnalyzer()
    obj._check_data(url)
