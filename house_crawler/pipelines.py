# -*- coding: utf-8 -*-
from django.db import IntegrityError
from houses.models import House
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
        clean_str_list = ['title', 'description', 'address']
        for element in clean_int_list:
            item[element] = clean_int(item[element])
        for element in clean_str_list:
            if item[element]:
                item[element] = item[element].strip()

        # Fix #15 - Max size for title is 200, so to avoid errors truncate to 195
        if len(item['title']) > 195:
            item['title'] = item['title'][:195] + ' ...'

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
