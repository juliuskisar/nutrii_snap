import certifi
import settings
from pymongo import MongoClient

class ApplicationBootstrap:

    def get_mongo_client(self):
        ca = certifi.where()
        client = MongoClient(settings.MONGO["MONGO_HOST"], tlsCAFile=ca)
        return client[settings.MONGO["MONGO_DATABASE"]]
