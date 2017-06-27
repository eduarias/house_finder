# -*- coding: utf-8 -*-

import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
import logging


class MongoDBPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        for data in item:
            if not data:
                raise DropItem("Missing data!")
        self.collection.update({'url': item['url']}, {'$set': dict(item)}, upsert=True)
        logging.debug("Question added to MongoDB database!")

        return item

