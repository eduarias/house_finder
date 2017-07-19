__author__ = 'Eduardo Arias'
from home_crawler.items import FotocasaItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from datetime import datetime
import re


class FotocasaSpider(CrawlSpider):
    name = "fotocasa"
    allowed_domains = ["fotocasa.es"]

    start_urls = [
        'http://www.fotocasa.es/es/alquiler/casas/barcelona-capital/sarria-sant-gervasi/l',
    ]

    rules = (
        # Filter all the flats paginated by the website following the pattern indicated
        Rule(LinkExtractor(restrict_xpaths='//a[@class="sui-Pagination-link" and text()=">"]'),
             callback='parse_flat_list',
             follow=True),
        # Filter all flats
        # Rule(LinkExtractor(allow=('inmueble\.')), callback='parse_flats', follow=False)
    )

    def parse_flat_list(self, response):
        flats = response.xpath('//div[@class="re-Searchresult"]')

        for flat in flats.xpath('//a[@class="re-Searchresult-itemRow"]'):
            yield response.follow(flat, callback=self.parse_flat)

    def parse_flat(self, response):

        flat = {'id_fotocasa': self._clean_int(
                    response.xpath('//div[@id="detailReference"]/text()').extract()[0]
                    ),
                'title': response.xpath('//h1[@class="property-title"]/text()').extract()[0],
                'update_date': None,
                'url': response.url,
                'price':self._clean_int(
                    response.xpath('//span[@id="detail-quickaccess_property_price"]/b/text()').extract()[0]
                    ),
                'sqft_m2': self._clean_int(
                    response.xpath('//*[@id="litSurface"]//text()').extract()[0]
                    ),
                'rooms': self._clean_int(
                    response.xpath('//*[@id="litRooms"]//text()').extract()[0]
                    ),
                'baths': self._clean_int(
                    response.xpath('//*[@id="litBaths"]//text()').extract()[0]
                    ),
                'address': response.xpath("//div[@class='detail-section-content']/text()").extract()[0],
                'last_updated': datetime.now().strftime('%Y-%m-%d')
        }

        yield FotocasaItem(**flat)

    @staticmethod
    def _clean_int(text):
        number = re.sub("[^0-9]", "", text)
        return int(number)

    parse_start_url = parse_flat_list
