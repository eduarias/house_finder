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
    xpath_list_next = '//a[@class="sui-Pagination-link" and text()=">"]/@href'

    provider = 'fotocasa'

    def parse_house(self, response):
        house = super(FotocasaSpider, self).parse_house(response)

        house.update({'site_id': clean_int(self.extract_from_xpath(response, '//div[@id="detailReference"]/text()')),
                      'title': response.xpath('//h1[@class="property-title"]/text()').extract_first(),
                      'description': response.xpath('//div[@class="detail-section-content"]/p/text()').extract_first(),
                      'price': response.xpath(
                          '//span[@id="detail-quickaccess_property_price"]/b/text()').extract_first(),
                      'sqft_m2': response.xpath('//*[@id="litSurface"]//text()').extract_first(),
                      'rooms': response.xpath('//*[@id="litRooms"]//text()').extract_first(),
                      'baths': response.xpath('//*[@id="litBaths"]//text()').extract_first(),
                      'address': response.xpath('//div[@class="detail-section-content"]/text()').extract_first(),
                      })

        yield HouseItem(**house)

    def get_url(self, response, url):
        return response.urljoin(url)
