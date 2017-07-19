__author__ = 'Eduardo Arias'
from home_crawler.items import HabitacliaItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from datetime import datetime
import re


class HabitacliaSpider(CrawlSpider):
    name = "habitaclia"
    allowed_domains = ["habitaclia.com"]

    start_urls = [
        'https://www.habitaclia.com/alquiler-vivienda-en-barcelona-barrio_sant_gervasi___bonanova/provincia_barcelona-barcelones-area_6-sarria_sant_gervasi/listainmuebles.htm',
        'https://www.habitaclia.com/alquiler-vivienda-en-barcelona-barrio_sant_gervasi___galvany/provincia_barcelona-barcelones-area_6-sarria_sant_gervasi/listainmuebles.htm',
    ]

    rules = (
        # Filter all the flats paginated by the website following the pattern indicated
        Rule(LinkExtractor(restrict_xpaths=("//a[@class='siguiente']")),
             callback='parse_flat_list',
             follow=True),
        # Filter all flats
        # Rule(LinkExtractor(allow=('inmueble\.')), callback='parse_flats', follow=False)
    )

    def parse_flat_list(self, response):
        flats = response.xpath("//ul[@class='enlista']/li")

        for flat in flats.xpath("//a[@itemprop='name']"):
            yield response.follow(flat, callback=self.parse_flat)

    def parse_flat(self, response):
        info_data = response.xpath('//section[@class="summary bg-white"]//ul[@class="feature-container"]/li[@class="feature"]/strong/text()').extract()

        try:
            address = response.xpath("//div[@id='addressPromo']/ul/li/text()").extract()[0]
        except IndexError:
            address = None

        flat = {'id_habitaclia': self._clean_int(
                    response.xpath('//span[@class="detail-id"]/text()').extract()[0]
                    ),
                'title': response.xpath('//h1/text()').extract()[0],
                'update_date': None,
                'url': response.url,
                'price': self._clean_int(response.xpath("//div[@class='price']/span[@itemprop='price']/text()").extract()[0]),
                'sqft_m2': self._clean_int(info_data[0]),
                'rooms': self._clean_int(info_data[1]),
                'address': address,
                'baths': self._clean_int(info_data[2]),
                'last_updated': datetime.now().strftime('%Y-%m-%d')}

        yield HabitacliaItem(**flat)

    @staticmethod
    def _clean_int(text):
        number = re.sub("[^0-9]", "", text)
        return int(number)

    # Overriding parse_start_url to get the first page
    parse_start_url = parse_flat_list
