__author__ = 'Eduardo Arias'
from home_crawler.items import IdealistaItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from datetime import datetime
import re


class IdealistaSpider(CrawlSpider):
    name = "idealista"
    allowed_domains = ["idealista.com"]
    ########################################################################
    ###       Add the url to crawl in the start_urls variable           ###
    ########################################################################
    # start_urls = ["https://www.idealista.com/venta-viviendas/leganes/el-carrascal/"]
    # start_urls = ['https://www.idealista.com/alquiler-viviendas/madrid/zona-norte/']

    start_urls = [
        'https://www.idealista.com/alquiler-viviendas/barcelona/sarria-sant-gervasi/sant-gervasi-la-bonanova/',
    ]

    rules = (
        # Filter all the flats paginated by the website following the pattern indicated
        Rule(LinkExtractor(restrict_xpaths=("//a[@class='icon-arrow-right-after']")),
             callback='parse_flat_list',
             follow=True),
        # Filter all flats
        # Rule(LinkExtractor(allow=('inmueble\.')), callback='parse_flats', follow=False)
    )

    def parse_flat_list(self, response):
        flats = response.xpath("//div[@class='items-container']/article")

        for flat in flats.xpath("//a[@class='item-link ']"):
            yield response.follow(flat, callback=self.parse_flat)

    def parse_flat(self, response):
        info_data = response.xpath('//div[@id="js-head-second"]//ul[@class="feature-container"]/li[@class="feature"]/text()').extract()

        baths = self._clean_int(response.xpath(
            '//h2[text()="Características básicas"]/following-sibling::ul/li[contains(text(), "baño")]/text()')
                                .extract()[0])

        try:
            toilets = self._clean_int(response.xpath(
                '//h2[text()="Características básicas"]/following-sibling::ul/li[contains(text(), "aseo")]/text()')
                                      .extract()[0])
        except IndexError:
            toilets = 0

        baths += toilets

        flat = {'id_idealista': list(filter(None, response.url.split('/')))[-1],
                'title': response.xpath("//h1/span/text()").extract()[0].strip(),
                'update_date': response.xpath("//section[@id='stats']/p/text()").extract()[0],
                'url': response.url,
                'price': self._clean_int(response.xpath('//p[@class="price"]/text()').extract()[0]),
                'sqft_m2': self._clean_int(response.xpath('//div[@class="info-data"]/span[2]/span/text()')
                                           .extract()[0]),
                'rooms': self._clean_int(response.xpath('//div[@class="info-data"]/span[3]/span/text()')
                                         .extract()[0]),
                'address': None,
                'baths': baths,
                'last_updated': datetime.now().strftime('%Y-%m-%d')}

        yield IdealistaItem(**flat)

    @staticmethod
    def _clean_int(text):
        number = re.sub("[^0-9]", "", text)
        return int(number)

    # Overriding parse_start_url to get the first page
    parse_start_url = parse_flat_list
