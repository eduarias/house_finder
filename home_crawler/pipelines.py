# -*- coding: utf-8 -*-
import pymongo
from django.db import IntegrityError
from scrapy.conf import settings
from scrapy.exceptions import DropItem
import logging
from datetime import datetime
import re
from abc import abstractmethod


def clean_int(text):
    if text:
        if isinstance(text, str):
            number = re.sub("[^0-9]", "", text)
            if number:
                return int(number)
            else:
                logging.info('Empty text - Original text: {}'.format(text))
                return None
    else:
        return int(text)


class HomeBasePipeline(object):

    def process_item(self, item, spider):
        clean_int_list = ['price', 'sqft_m2', 'rooms', 'baths']
        for element in clean_int_list:
            item[element] = clean_int(item[element])
        item['title'] = item['title'].strip()
        if item['address']:
            item['address'] = item['address'].strip()

        self.post_process_item(item, spider)

    @abstractmethod
    def post_process_item(self, item, spider):
        raise NotImplementedError


class DjangoPipeline(HomeBasePipeline):

    def post_process_item(self, item, spider):
        try:
            item.save()
            logging.debug("Home added to Django database! {}".format(item['url']))
        except IntegrityError:
            logging.info("Url already in database: {}".format(item['url']))
        return item


class MongoDBPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def post_process_item(self, item, spider):
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
