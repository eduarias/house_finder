from house_crawler.items import HouseItem
from house_crawler.spiders.BaseSpider import BaseSpider
from house_crawler.pipelines import clean_int


class FotocasaSpider(BaseSpider):
    name = "fotocasa"
    allowed_domains = ["fotocasa.es"]
    download_delay = 3

    xpath_list = '//div[@class="re-Searchresult"]'
    xpath_list_item = './/div[@class="re-Searchresult-itemRow"]'
    xpath_list_item_href = './/a[@class="re-Card-link"]/@href'
    xpath_list_item_price = './/span[@class="re-Card-price"]/text()'
    xpath_list_next = '//a[contains(@class, "sui-PaginationBasic-link") and text()=">"]/@href'

    provider = 'fotocasa'

    def parse_houses_list(self, response):
        """
        Contract:
        @url https://www.fotocasa.es/es/alquiler/casas/barcelona-capital/sant-gervasi-galvany/l
        @returns items 0
        @returns requests 0
        """
        return super(FotocasaSpider, self).parse_houses_list(response)

    def parse_house(self, response):
        """
        Parses a house.
        :param response: HTML response of a house item
        :rtype: HouseItem

        Contract:
        @url https://www.fotocasa.es/vivienda/barcelona-capital/aire-acondicionado-calefaccion-terraza-ascensor-amueblado-parking-television-se-aceptan-mascotas-internet-prats-de-mollo-18-135215074?RowGrid=3&tti=3&opi=300  # noqa
        @returns items 1
        @returns requests 0
        @scrapes title url price rooms baths sqft_m2
        """
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
        return response.urljoin(url).split('?')[0]
