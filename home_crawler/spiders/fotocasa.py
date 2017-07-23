from home_crawler.items import HomeItem
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from home_crawler.spiders.BaseSpider import BaseSpider
from home_crawler.pipelines import clean_int


class FotocasaSpider(BaseSpider):
    name = "fotocasa"
    allowed_domains = ["fotocasa.es"]
    download_delay = 3

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

        for flat in flats.xpath('//div[@class="re-Searchresult-item"]//a[@class="re-Card-title"]'):
            yield response.follow(flat, callback=self.parse_flat)

    def parse_flat(self, response):

        flat = {'site_id': clean_int(self.extract_from_xpath(response, '//div[@id="detailReference"]/text()')),
                'website': 'Fotocasa',
                'title': self.extract_from_xpath(response, '//h1[@class="property-title"]/text()'),
                'url': response.url,
                'price': self.extract_from_xpath(response, '//span[@id="detail-quickaccess_property_price"]/b/text()'),
                'sqft_m2': self.extract_from_xpath(response, '//*[@id="litSurface"]//text()'),
                'rooms': self.extract_from_xpath(response, '//*[@id="litRooms"]//text()'),
                'baths': self.extract_from_xpath(response, '//*[@id="litBaths"]//text()'),
                'address': self.extract_from_xpath(response, "//div[@class='detail-section-content']/text()"),
        }

        yield HomeItem(**flat)

    parse_start_url = parse_flat_list
