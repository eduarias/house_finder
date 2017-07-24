from home_crawler.items import HomeItem
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from home_crawler.spiders.BaseSpider import BaseSpider
from home_crawler.pipelines import clean_int


class HabitacliaSpider(BaseSpider):

    name = "habitaclia"
    allowed_domains = ["habitaclia.com"]
    download_delay = 0.5

    xpath_list = '//ul[@class="enlista"]'
    xpath_list_item = './/li[@data-id]'
    xpath_list_item_href = './/a[@itemprop="name"]/@href'
    xpath_list_item_price = './/span[@itemprop="price"]/text()'

    start_urls = [
        'https://www.habitaclia.com/alquiler-vivienda-en-barcelona-barrio_sant_gervasi___bonanova/provincia_barcelona-barcelones-area_6-sarria_sant_gervasi/listainmuebles.htm',
        'https://www.habitaclia.com/alquiler-vivienda-en-barcelona-barrio_sant_gervasi___galvany/provincia_barcelona-barcelones-area_6-sarria_sant_gervasi/listainmuebles.htm',
    ]

    rules = (
        # Filter all the flats paginated by the website following the pattern indicated
        Rule(LinkExtractor(restrict_xpaths="//a[@class='siguiente']"),
             callback='parse_flat_list',
             follow=True),
    )

    def parse_flat(self, response):
        info_xpath = '//section[@class="summary bg-white"]//ul[@class="feature-container"]/li[@class="feature"]/strong/text()'

        try:
            address = self.extract_from_xpath(response, "//div[@id='addressPromo']/ul/li/text()")
        except IndexError:
            address = None

        flat = {'site_id': clean_int(response.xpath('//span[@class="detail-id"]/text()').extract_first()),
                'website': 'Habitaclia',
                'title': response.xpath('//h1/text()').extract_first(),
                'url': response.url.split('?')[0],
                'price': response.xpath("//div[@class='price']/span[@itemprop='price']/text()").extract_first(),
                'sqft_m2': self.extract_from_xpath(response, info_xpath, 0),
                'rooms': self.extract_from_xpath(response, info_xpath, 1),
                'address': address,
                'baths': self.extract_from_xpath(response, info_xpath, 2),
                }

        yield HomeItem(**flat)

    def get_url(self, response, url):
        return url.split('?')[0]
