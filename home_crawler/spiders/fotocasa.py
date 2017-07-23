from home_crawler.items import HomeItem
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from home_crawler.spiders.BaseSpider import BaseSpider


class FotocasaSpider(BaseSpider):
    name = "fotocasa"
    allowed_domains = ["fotocasa.es"]
    download_delay = 0.5

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

        for flat in flats.xpath('//a[@class="re-Searchresult-item"]'):
            yield response.follow(flat, callback=self.parse_flat)

    def parse_flat(self, response):

        flat = {'site_id': self._clean_int(
                    response.xpath('//div[@id="detailReference"]/text()').extract()[0]
                    ),
                'website': 'Fotocasa',
                'title': response.xpath('//h1[@class="property-title"]/text()').extract()[0],
                'url': response.url,
                'price': self._clean_int(
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
        }

        yield HomeItem(**flat)

    parse_start_url = parse_flat_list
