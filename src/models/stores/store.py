import uuid

from src.common.database import Database
import src.models.stores.Constants as StoreConstants
import src.models.stores.Errors as StoreErrors


class Store(object):
    def __init__(self,name, url_prefix,tag_name,query, _id = None):
        self.name = name
        self.url_prefix = url_prefix
        self.tag_name = tag_name
        self.query = query
        self._id = uuid.uuid4().hex if _id is None else _id



    def __repr__(self):
        return "<Store {}>".format(self.name)

    def json(self):
        return{
            "_id":self._id,
            "name":self.name,
            "url_prefix":self.url_prefix,
            "tag_name":self.tag_name,
            "query":self.query
        }

    def save_to_mongo(self):
        Database.update( StoreConstants.COLLECTION, {"_id":self._id},self.json())

    @classmethod
    def get_by_id(cls, _id):
        return cls(**Database.find_one(collection= StoreConstants.COLLECTION, query = {"_id":_id}))

    @classmethod
    def get_by_name(cls,name):
        return cls(**Database.find_one(collection= StoreConstants.COLLECTION, query= {"name":name}))

    @classmethod
    def get_by_urlprefix(cls,url_prefix):
        #they give: hhtp://www.john
        #return:http:www.johnlewis
        return cls(**Database.find_one(collection=StoreConstants.COLLECTION, query={"url_prefix": {"$regex":'^{}'.format(url_prefix)}}))#the {} here will put url_prefix into regex

    @classmethod
    def find_by_url(cls, url):
        #url: the item url
        for i in range(0, len(url)+1):
            try:
                store = cls.get_by_urlprefix(url[:i])
                return  store
            except:
                raise StoreErrors.StoreNotFoundException("The url can not find a store")

    @classmethod
    def find_all(cls):
        return [cls(**elem) for elem in Database.find(StoreConstants.COLLECTION,{})]

    def remove(self):
        Database.delete(StoreConstants.COLLECTION,{"_id":self._id})

