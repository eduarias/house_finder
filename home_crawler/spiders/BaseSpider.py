from abc import abstractmethod

from scrapy.spiders import CrawlSpider


class BaseSpider(CrawlSpider):

    xpath_list = None
    xpath_list_item = None
    xpath_list_item_href = None
    xpath_list_item_price = None

    def parse_flat_list(self, response):
        """
        From a list of houses, get a single house and send it to parse_flat crawler
        :param response: HTTP response of the houses list
        :return: Callback for a single house crawling
        """

        flats = response.xpath(self.xpath_list)
        for flat in flats.xpath(self.xpath_list_item):
            url = flat.xpath(self.xpath_list_item_href).extract_first()
            house_url = self.get_url(response, url)
            if not self.is_url_in_db(house_url):
                yield response.follow(house_url, callback=self.parse_flat)
            else:
                price = flat.xpath(self.xpath_list_item_price).extract_first()
                self.update_price(house_url, price)

    @abstractmethod
    def get_url(self, response, url):
        raise NotImplementedError

    @abstractmethod
    def parse_flat(self, response):
        """
        Parse the house
        :param response: HTTP response of a single house
        :return: A HomeItem object with the home data to be pipelined.
        :rtype: HomeItem
        """
        raise NotImplementedError

    @staticmethod
    def extract_from_xpath(response, xpath, index=0):
        values = response.xpath(xpath).extract()
        try:
            return values[index]
        except IndexError:
            return None

    parse_start_url = parse_flat_list
