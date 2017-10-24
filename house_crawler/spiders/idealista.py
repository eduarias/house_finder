from house_crawler.items import HouseItem
from house_crawler.spiders.BaseSpider import BaseSpider
from house_crawler.pipelines import clean_int


class IdealistaSpider(BaseSpider):
    name = "idealista"
    allowed_domains = ["idealista.com"]
    download_delay = 3

    xpath_list = '//div[@class="items-container"]/article'
    xpath_list_item = './/div[@class="item-info-container"]'
    xpath_list_item_href = './/a[@class="item-link "]/@href'
    xpath_list_item_price = './/span[@class="item-price"]/text()'
    xpath_list_next = "//a[@class='icon-arrow-right-after']"

    provider = 'idealista'

    def parse_house(self, response):
        baths_xpath = '//h2[text()="Características básicas"]/following-sibling::ul/li[contains(text(), "baño")]' \
                      '/text()'
        baths = clean_int(self.extract_from_xpath(response, baths_xpath))

        toilets_xpath = \
            '//h2[text()="Características básicas"]/following-sibling::ul/li[contains(text(), "aseo")]/text()'
        try:
            toilets = clean_int(self.extract_from_xpath(response, toilets_xpath))
        except IndexError:
            toilets = 0

        if toilets:
            baths += toilets

        house = {'site_id': list(filter(None, response.url.split('/')))[-1],
                 'title': response.xpath("//h1/span/text()").extract_first(),
                 'start_url': response.meta['start_url'],
                 'description': response.xpath(
                     '//section[@id="details"]//div[@class="adCommentsLanguage expandable"]/text()').extract_first(),
                 'article_update_date': response.xpath("//section[@id='stats']/p/text()").extract_first(),
                 'url': response.url,
                 'price': response.xpath('//p[@class="price"]/text()').extract_first(),
                 'sqft_m2': response.xpath('//div[@class="info-data"]/span[2]/span/text()').extract_first(),
                 'rooms': response.xpath('//div[@class="info-data"]/span[3]/span/text()').extract_first(),
                 'address': None,
                 'baths': baths,
                 }

        yield HouseItem(**house)

    def get_url(self, response, url):
        return response.urljoin(url)
