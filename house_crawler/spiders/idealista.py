from house_crawler.items import HouseItem
from house_crawler.spiders.BaseSpider import BaseSpider
from house_crawler.pipelines import clean_int


class IdealistaSpider(BaseSpider):
    name = "idealista"
    allowed_domains = ["idealista.com"]
    download_delay = 10

    xpath_list = '//div[@class="items-container"]/article'
    xpath_list_item = './/div[@class="item-info-container"]'
    xpath_list_item_href = './/a[@class="item-link "]/@href'
    xpath_list_item_price = './/span[@class="item-price"]/text()'
    xpath_list_next = "//a[@class='icon-arrow-right-after']/@href"

    provider = 'idealista'

    # Custom Xpath
    baths_xpath = '//h2[text()="Características básicas"]/following-sibling::ul/li[contains(text(), "baño")]/text()'
    toilets_xpath = \
        '//h2[text()="Características básicas"]/following-sibling::ul/li[contains(text(), "aseo")]/text()'

    def parse_houses_list(self, response):
        """
        Contract:
        @url https://www.idealista.com/alquiler-viviendas/barcelona/sarria-sant-gervasi/sant-gervasi-la-bonanova/
        @returns items 0
        @returns requests 0
        """
        return super(IdealistaSpider, self).parse_houses_list(response)

    def parse_house(self, response):
        """
        Parses a house.
        :param response: HTML response of a house item
        :rtype: HouseItem

        Contract:
        @url https://www.idealista.com/inmueble/25078492/
        @returns items 1
        @returns requests 0
        @scrapes title url price rooms baths sqft_m2
        """
        house = super(IdealistaSpider, self).parse_house(response)

        baths = clean_int(self.extract_from_xpath(response, self.baths_xpath))

        try:
            toilets = clean_int(self.extract_from_xpath(response, self.toilets_xpath))
        except IndexError:
            toilets = 0

        if toilets:
            baths += toilets

        house.update({'site_id': list(filter(None, response.url.split('/')))[-1],
                      'title': response.xpath("//h1/span/text()").extract_first(),
                      'description': response.xpath(
                          '//section[@id="details"]//div[@class="adCommentsLanguage expandable"]/text()').
                     extract_first(),
                      'article_update_date': response.xpath("//section[@id='stats']/p/text()").extract_first(),
                      'price': response.xpath('//p[@class="price"]/text()').extract_first(),
                      'sqft_m2': response.xpath('//div[@class="info-data"]/span[2]/span/text()').extract_first(),
                      'rooms': response.xpath('//div[@class="info-data"]/span[3]/span/text()').extract_first(),
                      'address': None,
                      'baths': baths,
                      })

        yield HouseItem(**house)

    def get_url(self, response, url):
        return response.urljoin(url)
