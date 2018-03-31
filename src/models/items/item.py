import uuid

import requests
from bs4 import BeautifulSoup
import re
import src.models.items.constants as ItemConstants

from src.common.database import Database
from src.models.stores.store import Store


class Item(object):
    def __init__(self, name, url, _id = None , price = None):
        self.name = name
        self.url = url
        store = Store.find_by_url(url)
        self.tag_name = store.tag_name
        self.query = store.query
        self.price = None if price is None else price
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Item {} with url {}>".format(self.name, self.url)

    #Amazon:<span class="buyingPrice">299</span>
    def load_price(self):
        request = requests.get(self.url)
        content= request.content
        soup = BeautifulSoup(content,"html.parser")
        element = soup.find(self.tag_name, self.query)
        string_price = element.text.strip()

        pattern = re.compile('(\d+.\d+)')
        match = pattern.search(string_price)
        self.price = float(match.group())
        return self.price

    def save_to_mongo(self):
        Database.update(ItemConstants.COLLECTION, {"_id":self._id},self.json())

    def json(self):
        return{
            "name":self.name,
            "url":self.url,
            "_id":self._id,
            "price":self.price
        }

    @classmethod
    def from_mongo(cls,_id):
        theitem = Database.find_one(collection= ItemConstants.COLLECTION,query={'_id':_id})
        return cls(**theitem)

    @classmethod
    def get_by_id(cls,item_id):
        return cls(**Database.find_one(collection= ItemConstants.COLLECTION, query={'_id': item_id}))