from scrapy.spiders import CrawlSpider


class BaseSpider(CrawlSpider):

    @staticmethod
    def extract_from_xpath(response, xpath, index=0):
        values = response.xpath(xpath).extract()
        if values:
            return values[index]
        else:
            return None
