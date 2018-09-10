""""Abstract class to crawl real state sites"""
import urllib.parse
from abc import abstractmethod
import logging

from scrapy.spiders import CrawlSpider
from scrapy.http import Request

from houses.models import StartURL, HousesProvider


class BaseSpider(CrawlSpider):

    xpath_list = None
    xpath_list_item = None
    xpath_list_item_href = None
    xpath_list_item_price = None
    xpath_list_next = None

    provider = None

    def parse_houses_list(self, response):
        """
        From a list of houses, get a single house and send it to parse_houses crawler
        :param response: HTTP response of the houses list
        :return: Callback for a single house crawling
        """

        houses = response.xpath(self.xpath_list)
        start_url = self.get_start_url_from_meta(response)

        for house in houses.xpath(self.xpath_list_item):
            url = house.xpath(self.xpath_list_item_href).extract_first()
            house_url = self.get_url(response, url)
            house_url = urllib.parse.quote(house_url, safe=':/?&=')

            if not self.is_url_in_db(house_url):
                logging.debug('Url not in database: {}'.format(house_url))
                yield response.follow(house_url, meta={'start_url': start_url}, callback=self.parse_house)
            else:
                price = house.xpath(self.xpath_list_item_price).extract_first()
                self.update_house(house_url, price)

        next_page = response.xpath(self.xpath_list_next).extract_first()
        if next_page is not None:
            yield response.follow(next_page, meta={'start_url': start_url}, callback=self.parse_houses_list)

    @abstractmethod
    def get_url(self, response, url):
        raise NotImplementedError

    def parse_house(self, response):
        """
        Parse the house
        :param response: HTTP response of a single house
        :return: A HouseItem object with the home data to be pipelined.
        :rtype: HouseItem
        """
        house = {
            'url': response.url,
            'start_url': self.get_start_url_from_meta(response),
        }

        return house

    @staticmethod
    def extract_from_xpath(response, xpath, index=0):
        values = response.xpath(xpath).extract()
        try:
            return values[index]
        except IndexError:
            return None

    def start_requests(self):
        """Get the start urls to begin crawling"""
        _house_provider = HousesProvider.objects.get(name=self.provider)
        for start_url in StartURL.objects.filter(provider=_house_provider):
            yield Request(start_url.url, meta={'start_url': start_url}, dont_filter=True)

    @staticmethod
    def get_start_url_from_meta(response):
        return response.meta.get('start_url', None)

    parse_start_url = parse_houses_list
