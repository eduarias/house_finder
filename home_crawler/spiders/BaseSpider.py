from scrapy.contrib.spiders import CrawlSpider
import re


class BaseSpider(CrawlSpider):

    @staticmethod
    def _clean_int(text):
        number = re.sub("[^0-9]", "", text)
        return int(number)
