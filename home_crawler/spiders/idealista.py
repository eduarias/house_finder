from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from home_crawler.items import HomeItem
from home_crawler.spiders.BaseSpider import BaseSpider
from home_crawler.pipelines import clean_int


class IdealistaSpider(BaseSpider):
    name = "idealista"
    allowed_domains = ["idealista.com"]
    download_delay = 3

    xpath_list = '//div[@class="items-container"]/article'
    xpath_list_item = './/div[@class="item-info-container"]'
    xpath_list_item_href = './/a[@class="item-link "]/@href'
    xpath_list_item_price = './/span[@class="item-price"]/text()'

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
                'title': response.xpath("//h1/span/text()").extract_first(),
                'article_update_date': response.xpath("//section[@id='stats']/p/text()").extract_first(),
                'url': response.url,
                'price': response.xpath('//p[@class="price"]/text()').extract_first(),
                'sqft_m2': response.xpath('//div[@class="info-data"]/span[2]/span/text()').extract_first(),
                'rooms': response.xpath('//div[@class="info-data"]/span[3]/span/text()').extract_first(),
                'address': None,
                'baths': baths,
                }

        yield HomeItem(**flat)

    def get_url(self, response, url):
        return response.urljoin(url)
