# -*- coding: utf-8 -*-

import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
import logging
from datetime import datetime


class MongoDBPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        today = datetime.now().strftime('%Y-%m-%d')

        # Minimum data scraped to be in DB
        basic_data = ['price', 'sqft_m2', 'rooms']
        for data in basic_data:
            if not item[data]:
                raise DropItem("Missing data: {}!".format(data))

        self.collection.update({'url': item['url']},
                               {'$set': dict(item),
                                '$setOnInsert': {'found_on': today}},
                               upsert=True)
        logging.debug("Home {} added to MongoDB database!".format(item['url']))

        return item
