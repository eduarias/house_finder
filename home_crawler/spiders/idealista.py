from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from home_crawler.items import HomeItem
from home_crawler.spiders.BaseSpider import BaseSpider
from home_crawler.pipelines import clean_int


class IdealistaSpider(BaseSpider):
    name = "idealista"
    allowed_domains = ["idealista.com"]
    download_delay = 3

    start_urls = [
        'https://www.idealista.com/alquiler-viviendas/barcelona/sarria-sant-gervasi/sant-gervasi-la-bonanova/',
    ]

    rules = (
        # Filter all the flats paginated by the website following the pattern indicated
        Rule(LinkExtractor(restrict_xpaths="//a[@class='icon-arrow-right-after']"),
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

        baths = clean_int(self.extract_from_xpath(response,
            '//h2[text()="Características básicas"]/following-sibling::ul/li[contains(text(), "baño")]/text()'))

        try:
            toilets = clean_int(self.extract_from_xpath(response,
                '//h2[text()="Características básicas"]/following-sibling::ul/li[contains(text(), "aseo")]/text()'))
        except IndexError:
            toilets = 0

        if toilets:
            baths += toilets

        flat = {'site_id': list(filter(None, response.url.split('/')))[-1],
                'website': 'Idealista',
                'title': self.extract_from_xpath(response, "//h1/span/text()"),
                'article_update_date': self.extract_from_xpath(response, "//section[@id='stats']/p/text()"),
                'url': response.url,
                'price': self.extract_from_xpath(response, '//p[@class="price"]/text()'),
                'sqft_m2': self.extract_from_xpath(response, '//div[@class="info-data"]/span[2]/span/text()'),
                'rooms': self.extract_from_xpath(response, '//div[@class="info-data"]/span[3]/span/text()'),
                'address': None,
                'baths': baths,
                }

        yield HomeItem(**flat)

    # Overriding parse_start_url to get the first page
    parse_start_url = parse_flat_list
