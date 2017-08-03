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
        # 'Ciudad Jardín': 'https://www.fotocasa.es/es/alquiler/casas/las-palmas-de-gran-canaria/ciudad-jardin/l',
        # 'Arenales - Lugo': 'https://www.fotocasa.es/es/alquiler/casas/las-palmas-de-gran-canaria/arenales-lugo-avda-maritima/l',
    }

    def parse_house(self, response):

        house = {'site_id': clean_int(self.extract_from_xpath(response, '//div[@id="detailReference"]/text()')),
                'website': 'Fotocasa',
                'title': response.xpath('//h1[@class="property-title"]/text()').extract_first().strip(),
                'neighborhood': response.meta['neighborhood'],
                'description': response.xpath('//div[@class="detail-section-content"]/p/text()').extract_first(),
                'url': response.url,
                'price': response.xpath('//span[@id="detail-quickaccess_property_price"]/b/text()').extract_first(),
                'sqft_m2': response.xpath('//*[@id="litSurface"]//text()').extract_first(),
                'rooms': response.xpath('//*[@id="litRooms"]//text()').extract_first(),
                'baths': response.xpath('//*[@id="litBaths"]//text()').extract_first(),
                'address': response.xpath('//div[@class="detail-section-content"]/text()').extract_first(),
        }

        yield HouseItem(**house)

    def get_url(self, response, url):
        return response.urljoin(url)