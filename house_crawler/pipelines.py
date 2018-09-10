import logging
import re
from abc import abstractmethod

from django.db import IntegrityError
from django.utils import timezone

from houses.models import House
from scrapy.exceptions import DropItem


def clean_int(text):
    """
    From a text remove everything that is not a number
    :param text: Input text
    :return: An integer with all number characters from text
    :rtype: int or None
    """
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
    """Abstract class to clean, validate and save scrapped data """

    def process_item(self, item, spider):
        """
        This method is called for every item pipeline component.
        :param item: The item scraped
        :type item: Item or dict
        :param spider: The spider which scraped the item
        :type spider: Spider
        :return: HouseItem
        """
        clean_int_list = ['price', 'sqft_m2', 'rooms', 'baths']
        clean_str_list = ['title', 'description', 'address']

        for element in clean_int_list:
            item[element] = clean_int(item[element])

        for element in clean_str_list:
            if item[element]:
                item[element] = item[element].strip()

        # Fix #15 - Max size for title is House.TITLE_MAX_LENGTH, so to avoid errors truncate title if longest
        max_length = House.TITLE_MAX_LENGTH - 5
        if item['title'] and len(item['title']) > max_length:
            item['title'] = item['title'][:max_length] + ' ...'

        return self.post_process_item(item, spider)

    @abstractmethod
    def post_process_item(self, item, spider):
        """
        Specific tasks for process_item done by a pipeline
        :param item: Item to be saved
        :type item: HouseItem
        :param spider: Spider
        :type spider: Spider
        :return: HouseItem
        """
        raise NotImplementedError

    def is_url_in_db(self, url):
        """
        Check if the URL already exists in the database.
        :param url: URL to search for
        :type url: str
        :return: True if exists
        :rtype: bool
        """
        raise NotImplementedError

    def open_spider(self, spider):
        """
        Method called when spider is opened.
        Set new methods required in the Spider
        :param spider: Spider
        """
        spider.is_url_in_db = self.is_url_in_db
        spider.update_house = self.update_house

    @abstractmethod
    def update_house(self, url, price):
        """
        Update item
        :param url: Item url
        :param price: Current price
        :return: None
        """
        raise NotImplementedError


class DjangoPipeline(HouseBasePipeline):
    """Pipeline to use with Django ORM"""

    def post_process_item(self, item, spider):
        try:
            item['updated_at'] = timezone.now()
            item.save()
            logging.debug("House added to Django database! {}".format(item['url']))
        except IntegrityError as e:
            logging.error("Error inserting into database - url: {}\n\t{}".format(item['url'], str(e)))
            raise DropItem
        return item

    def is_url_in_db(self, url):
        return House.objects.filter(url=url).exists()

    def update_house(self, url, price):
        house = House.objects.get(url=url)
        price = clean_int(price)
        if house.price != price:
            logging.info('Url already in database: {}, updating price: {}'.format(url, price))
            house.price = price
            house.updated_at = timezone.now()
        else:
            logging.info('Url already in database: {}, updating last view'.format(url))
        house.save()
