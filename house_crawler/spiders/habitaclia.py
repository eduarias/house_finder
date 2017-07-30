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

    start_urls_neighborhoods = {
        'Sant Gervasi - Bonanova': 'https://www.habitaclia.com/alquiler-vivienda-en-barcelona-barrio_sant_gervasi___bonanova/provincia_barcelona-barcelones-area_6-sarria_sant_gervasi/listainmuebles.htm',
        'Sant Gervasi - Galvany': 'https://www.habitaclia.com/alquiler-vivienda-en-barcelona-barrio_sant_gervasi___galvany/provincia_barcelona-barcelones-area_6-sarria_sant_gervasi/listainmuebles.htm',
    }



    def parse_house(self, response):
        info_xpath = '//section[@class="summary bg-white"]//ul[@class="feature-container"]/li[@class="feature"]/strong/text()'

        try:
            address = self.extract_from_xpath(response, "//div[@id='addressPromo']/ul/li/text()")
        except IndexError:
            address = None

        house = {'site_id': clean_int(response.xpath('//span[@class="detail-id"]/text()').extract_first()),
                'website': 'Habitaclia',
                'title': response.xpath('//h1/text()').extract_first(),
                'neighborhood': response.meta['neighborhood'],
                'url': response.url.split('?')[0],
                'price': response.xpath("//div[@class='price']/span[@itemprop='price']/text()").extract_first(),
                'sqft_m2': self.extract_from_xpath(response, info_xpath, 0),
                'rooms': self.extract_from_xpath(response, info_xpath, 1),
                'address': address,
                'baths': self.extract_from_xpath(response, info_xpath, 2),
                }

        yield HouseItem(**house)

    def get_url(self, response, url):
        return url.split('?')[0]
