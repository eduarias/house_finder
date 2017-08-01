from abc import abstractmethod

from scrapy.spiders import CrawlSpider
from scrapy.http import Request


class BaseSpider(CrawlSpider):

    xpath_list = None
    xpath_list_item = None
    xpath_list_item_href = None
    xpath_list_item_price = None
    xpath_list_next = None

    start_urls_neighborhoods = None

    def parse_houses_list(self, response):
        """
        From a list of houses, get a single house and send it to parse_houses crawler
        :param response: HTTP response of the houses list
        :return: Callback for a single house crawling
        """

        houses = response.xpath(self.xpath_list)
        neighborhood = response.meta.get('neighborhood', None)

        for house in houses.xpath(self.xpath_list_item):
            url = house.xpath(self.xpath_list_item_href).extract_first()
            house_url = self.get_url(response, url)

            if not self.is_url_in_db(house_url):
                yield response.follow(house_url, meta={'neighborhood': neighborhood}, callback=self.parse_house)
            else:
                price = house.xpath(self.xpath_list_item_price).extract_first()
                self.update_price(house_url, price)
        next_page = response.xpath(self.xpath_list_next).extract_first()
        if next_page is not None:
            yield response.follow(next_page, meta={'neighborhood': neighborhood}, callback=self.parse_houses_list)

    @abstractmethod
    def get_url(self, response, url):
        raise NotImplementedError

    @abstractmethod
    def parse_house(self, response):
        """
        Parse the house
        :param response: HTTP response of a single house
        :return: A HouseItem object with the home data to be pipelined.
        :rtype: HouseItem
        """
        raise NotImplementedError

    @staticmethod
    def extract_from_xpath(response, xpath, index=0):
        values = response.xpath(xpath).extract()
        try:
            return values[index]
        except IndexError:
            return None

    def start_requests(self):
        for neighborhood, url in self.start_urls_neighborhoods.items():
            yield Request(url, meta={'neighborhood': neighborhood}, dont_filter=True)

    parse_start_url = parse_houses_list
