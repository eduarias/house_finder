from house_crawler.items import HouseItem
from house_crawler.spiders.BaseSpider import BaseSpider
from house_crawler.pipelines import clean_int


class HabitacliaSpider(BaseSpider):
    name = "habitaclia"
    allowed_domains = ["habitaclia.com"]
    download_delay = 0.5

    xpath_list = '//ul[@class="enlista"]'
    xpath_list_item = './/li[@data-id]'
    xpath_list_item_href = './/a[@itemprop="name"]/@href'
    xpath_list_item_price = './/span[@itemprop="price"]/text()'
    xpath_list_next = '//a[@class="siguiente"]/@href'

    provider = 'habitaclia'

    def parse_houses_list(self, response):
        """
        Contract:
        @url https://www.habitaclia.com/alquiler-sant_gervasi___bonanova-barcelona-1.htm
        @returns items 0
        @returns requests 0
        """
        super(HabitacliaSpider, self).parse_houses_list(response)

    def parse_house(self, response):
        """
        Parses a house.
        :param response: HTML response of a house item
        :rtype: HouseItem

        Contract:
        @url https://www.habitaclia.com/alquiler-casa-preciosa_en_bonanova_sant_gervasi_bonanova-barcelona-i3978002020033.htm  # noqa
        @returns items 1
        @returns requests 0
        @scrapes title url price rooms baths sqft_m2
        """
        info_xpath = '//section[@class="summary bg-white"]//ul[@class="feature-container"]/li[@class="feature" ' \
                     'and contains(., "{}")]//text()'

        try:
            address = self.extract_from_xpath(response, "//div[@id='addressPromo']/ul/li/text()")
        except IndexError:
            address = None

        house = {'site_id': clean_int(response.xpath('//span[@class="detail-id"]/text()').extract_first()),
                 'title': response.xpath('//h1/text()').extract_first(),
                 'start_url': self.get_start_url_from_meta(response),
                 'description': response.xpath('//p[@id="js-detail-description"]/text()').extract_first(),
                 'url': response.url.split('?')[0],
                 'price': response.xpath("//div[@class='price']/span[@itemprop='price']/text()").extract_first(),
                 'sqft_m2': self.extract_from_xpath(response, info_xpath.format("m"), 1),
                 'rooms': self.extract_from_xpath(response, info_xpath.format("hab."), 1),
                 'address': address,
                 'baths': self.extract_from_xpath(response, info_xpath.format("baño"), 1),
                 }

        yield HouseItem(**house)

    def get_url(self, response, url):
        return url.split('?')[0]
