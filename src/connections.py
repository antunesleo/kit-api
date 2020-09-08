""""
This module hold all the applications connections as databases"""
import pymongo
from flask import Flask

from src import configurations

config = configurations.get_config()
mongo_client = None
mongo_kit_db = None


def register(web_app: Flask) -> None:
    '''
        The initializer class should call this method to create the connections
    :param web_app:
    :return:
    '''
    global mongo_client
    global mongo_kit_db
    mongo_client = pymongo.MongoClient(config.MONGO_HOST, config.MONGO_PORT)
    mongo_kit_db = mongo_client['kit']
    mongo_kit_db.products.create_index("sku", unique=True)
    mongo_kit_db.kits.create_index("sku", unique=True)
