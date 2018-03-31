import uuid

import datetime
import requests
import src.models.alerts.constants as AlertConstant
from src.common.database import Database
from src.models.items.item import Item


class Alert(object):
    def __init__(self, user_email, price_limit,item_id,active = True,_id = None, last_checked = None):
        self.user_email = user_email
        self.price_limit = price_limit
        self.item = Item.get_by_id(item_id)
        self.active = active
        #the urcnow is confusing here
        self.last_checked = datetime.datetime.utcnow() if last_checked is None else last_checked
        self._id = uuid.uuid4().hex if _id is None else _id


    def __repr__(self):
        return  "<Alert for {} on item {} with price {}>".format(self.user_email, self.item.name, self.price_limit)

    def send(self):
        requests.post(
            AlertConstant.URL,
            auth=("api",AlertConstant.API_KEY),
            data = {
                "from":AlertConstant.FROM,
                "to":self.user_email,
                "subject":"Your item reached price limit",
                "text": "Your {} reached price limit, pleas check with {}".format(self.item.name , self.item.url)
            }
        )

    @classmethod
    #find necessary updates
    def find_needing_update(cls, minute_since_update = AlertConstant.Alert_time):
        last_updated_limt = datetime.datetime.utcnow() - datetime.timedelta(minutes= minute_since_update)
        return [cls(**elem) for elem in Database.find(AlertConstant.COLLECTION, {"last_checked": {"$lte":last_updated_limt}, "active":True})]

    def save_to_mongo(self):
        Database.update(AlertConstant.COLLECTION,{"_id":self._id},self.json())

    def json(self):
        return {
            "_id": self._id,
            "price_limit":self.price_limit,
            "last_checked":self.last_checked,
            "user_email":self.user_email,
            "item_id":self.item._id,
            "active":self.active
        }

    def load_item_price(self):
        self.item.load_price()
        self.last_checked = datetime.datetime.utcnow()
        self.item.save_to_mongo()
        self.save_to_mongo()
        return self.item.price

    def send_message_when_reached(self):
        if self.item.price < self.price_limit:
            self.send()

    @classmethod
    def get_by_user_email(cls,user_email):
        return [cls(**elem) for elem in Database.find(AlertConstant.COLLECTION, {"user_email":user_email})]

    @classmethod
    def get_by_alert_id(cls,alert_id):
        return cls(**Database.find_one(AlertConstant.COLLECTION, {"_id":alert_id}))

    def deactivate_alert(self):
        self.active = False
        self.save_to_mongo()

    def delete_alert(self):
        Database.delete(AlertConstant.COLLECTION, {"_id":self._id})

    def activate_alert(self):
        self.active = True
        self.save_to_mongo()
