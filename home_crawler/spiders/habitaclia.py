from home_crawler.items import HabitacliaItem
from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors import LinkExtractor
from datetime import datetime
from home_crawler.spiders.BaseSpider import BaseSpider


class HabitacliaSpider(BaseSpider):
    name = "habitaclia"
    allowed_domains = ["habitaclia.com"]
    download_delay = 0.5

    start_urls = [
        'https://www.habitaclia.com/alquiler-vivienda-en-barcelona-barrio_sant_gervasi___bonanova/provincia_barcelona-barcelones-area_6-sarria_sant_gervasi/listainmuebles.htm',
        'https://www.habitaclia.com/alquiler-vivienda-en-barcelona-barrio_sant_gervasi___galvany/provincia_barcelona-barcelones-area_6-sarria_sant_gervasi/listainmuebles.htm',
    ]

    rules = (
        # Filter all the flats paginated by the website following the pattern indicated
        Rule(LinkExtractor(restrict_xpaths=("//a[@class='siguiente']")),
             callback='parse_flat_list',
             follow=True),
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
                'url': response.url.split('?')[0],
                'price': self._clean_int(response.xpath("//div[@class='price']/span[@itemprop='price']/text()").extract()[0]),
                'sqft_m2': self._clean_int(info_data[0]),
                'rooms': self._clean_int(info_data[1]),
                'address': address,
                'baths': self._clean_int(info_data[2]),
                'last_updated': datetime.now().strftime('%Y-%m-%d')}

        yield HabitacliaItem(**flat)

    # Overriding parse_start_url to get the first page
    parse_start_url = parse_flat_list
