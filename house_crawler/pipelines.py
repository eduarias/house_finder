# -*- coding: utf-8 -*-
import pymongo
from django.db import IntegrityError
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from store_houses.models import House
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
        elif isinstance(text, int):
            return text
    else:
        return None


class HouseBasePipeline(object):

    def process_item(self, item, spider):
        clean_int_list = ['price', 'sqft_m2', 'rooms', 'baths']
        for element in clean_int_list:
            item[element] = clean_int(item[element])
        item['title'] = item['title'].strip()
        if item['address']:
            item['address'] = item['address'].strip()

        return self.post_process_item(item, spider)

    @abstractmethod
    def post_process_item(self, item, spider):
        raise NotImplementedError

    def is_url_in_db(self, url):
        raise NotImplementedError

    def open_spider(self, spider):
        spider.is_url_in_db = self.is_url_in_db
        spider.update_price = self.update_price

    @abstractmethod
    def update_price(self, url, price):
        raise NotImplementedError


class DjangoPipeline(HouseBasePipeline):

    def post_process_item(self, item, spider):
        try:
            item.save()
            logging.debug("House added to Django database! {}".format(item['url']))
        except IntegrityError:
            logging.info("Url already in database: {}".format(item['url']))
        return item

    def is_url_in_db(self, url):
        try:
            house = House.objects.get(url=url)
        except House.DoesNotExist:
            house = None
        return True if house else False

    def update_price(self, url, price):
        house = House.objects.get(url=url)
        price = clean_int(price)
        logging.info('Url already in database: {}, updating price: {}'.format(url, price))
        house.price = price
        house.save()


class MongoDBPipeline(HouseBasePipeline):
    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def post_process_item(self, item, spider):
        today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Minimum data scraped to be in DB
        basic_data = ['price', 'sqft_m2', 'rooms']
        for data in basic_data:
            if not item[data]:
                raise DropItem("Missing data: {}!".format(data))

        item_to_db = dict(item)
        item_to_db['updated_at'] = today

        self.collection.update({'url': item['url']},
                               {'$set': item_to_db,
                                '$setOnInsert': {'created_at': today}},
                               upsert=True)
        logging.debug("House {} added to MongoDB database!".format(item['url']))

        return item

    def is_url_in_db(self, url):
        self.collection.find_one({"url": url})

    def update_price(self, url, price):
        self.collection.update({'url': 'url'}, {'$set': {'price': price}})
