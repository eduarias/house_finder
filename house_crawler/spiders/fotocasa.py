from house_crawler.items import HouseItem
from house_crawler.spiders.BaseSpider import BaseSpider
from house_crawler.pipelines import clean_int


class FotocasaSpider(BaseSpider):
    name = "fotocasa"
    allowed_domains = ["fotocasa.es"]
    download_delay = 3

    xpath_list = '//div[@class="re-Searchresult"]'
    xpath_list_item = './/div[@class="re-Searchresult-item"]'
    xpath_list_item_href = './/a[@class="re-Card-title"]/@href'
    xpath_list_item_price = './/span[@class="re-Card-price"]/text()'
    xpath_list_next = '//a[@class="sui-Pagination-link" and text()=">"]'

    start_urls_neighborhoods = {
        'Sarriá - Sant Gervasi': 'http://www.fotocasa.es/es/alquiler/casas/barcelona-capital/sarria-sant-gervasi/l',
    }

    def parse_house(self, response):

        house = {'site_id': clean_int(self.extract_from_xpath(response, '//div[@id="detailReference"]/text()')),
                'website': 'Fotocasa',
                'title': self.extract_from_xpath(response, '//h1[@class="property-title"]/text()'),
                'neighborhood': response.meta['neighborhood'],
                'url': response.url,
                'price': self.extract_from_xpath(response, '//span[@id="detail-quickaccess_property_price"]/b/text()'),
                'sqft_m2': self.extract_from_xpath(response, '//*[@id="litSurface"]//text()'),
                'rooms': self.extract_from_xpath(response, '//*[@id="litRooms"]//text()'),
                'baths': self.extract_from_xpath(response, '//*[@id="litBaths"]//text()'),
                'address': self.extract_from_xpath(response, "//div[@class='detail-section-content']/text()"),
        }

        yield HouseItem(**house)

    def get_url(self, response, url):
        return response.urljoin(url)