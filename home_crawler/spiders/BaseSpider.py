from scrapy.spiders import CrawlSpider


class BaseSpider(CrawlSpider):

    @staticmethod
    def extract_from_xpath(response, xpath, index=0):
        values = response.xpath(xpath).extract()
        try:
            return values[index]
        except IndexError:
            return None
