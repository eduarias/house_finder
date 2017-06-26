__author__ = 'Eduardo Arias'
from idealista.items import IdealistaItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from datetime import datetime
import re


class IdealistaSpider(CrawlSpider):
    name = "idealista"
    allowed_domains = ["idealista.com"]
    ########################################################################
    ###       Add the url to crawl in the start_urls variable           ###
    ########################################################################
    # start_urls = ["https://www.idealista.com/venta-viviendas/leganes/el-carrascal/"]
    # start_urls = ['https://www.idealista.com/alquiler-viviendas/madrid/zona-norte/']

    start_urls = ['https://www.idealista.com/alquiler-viviendas/barcelona/sarria-sant-gervasi/sant-gervasi-la-bonanova/']

    rules = (
        # Filter all the flats paginated by the website following the pattern indicated
        Rule(LinkExtractor(restrict_xpaths=("//a[@class='icon-arrow-right-after']")),
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
        flat = {}

        # Get last url parameter
        flat['id_idealista'] = list(filter(None, response.url.split('/')))[-1]

        flat['update_date'] = response.xpath("//section[@id='stats']/p/text()").extract()[0]

        flat['url'] = response.url

        info_data = response.xpath("//div[@class='info-data']//span/span/text()").extract()
        flat['price'] = self._clean_int(info_data[0])
        flat['sqft_m2'] = self._clean_int(info_data[1])
        flat['rooms'] = self._clean_int(info_data[2])

        flat['address'] = response.xpath("//div[@id='addressPromo']/ul/li/text()").extract()[0]

        baths_extract = response.xpath('//*[@id="details"]//li[contains(text(),"baño")]/text()').extract()[0]
        flat['baths'] = self._clean_int(baths_extract)

        flat['last_updated'] = datetime.now().strftime('%Y-%m-%d')

        yield IdealistaItem(**flat)

    @staticmethod
    def _clean_int(text):
        number = re.sub("[^0-9]", "", text)
        return int(number)

    # def parse_flats_old(self, response):
    #     # Necessary in order to create the whole link towards the website
    #     default_url = 'http://idealista.com'
    #
    #     info_flats_xpath = response.xpath("//*[@class='item-info-container']")
    #     prices_flats_xpath = response.xpath("//*[@class='row price-row clearfix']/span[@class='item-price']/text()")
    #     discounts_xpath = response.xpath("//*[@class='row price-row clearfix']")
    #
    #     links = [str(''.join(default_url + link.xpath('a/@href').extract().pop()))
    #              for link in info_flats_xpath]
    #
    #     prices = [float(flat.extract().replace('.', '').strip())
    #               for flat in prices_flats_xpath]
    #
    #     discounts = [0 if len(
    #         discount.xpath("./*[@class='item-price-down icon-pricedown']/text()").extract()) < 1 else discount.xpath(
    #         "./*[@class='item-price-down icon-pricedown']/text()").extract().pop().replace('.', '').strip().split(
    #         ' ').pop(0) for discount in discounts_xpath]
    #
    #     addresses = [address.xpath('a/@title').extract().pop().encode('iso-8859-1')
    #                  for address in info_flats_xpath]
    #
    #     rooms = [int(flat.xpath(
    #         'span[@class="item-detail"]/small[contains(text(),"hab.")]/../text()').extract().pop().strip()) if len(
    #         flat.xpath('span[@class="item-detail"]/small[contains(text(),"hab.")]')) == 1 else None for flat in
    #              info_flats_xpath]
    #
    #     baths_extract = response.xpath('//*[@id="details"]//li[contains(text(),"baño")]').extract()
    #
    #     baths = None if not baths_extract else int(baths_extract.pop())
    #
    #     sqfts_m2 = [float(
    #         flat.xpath('span[@class="item-detail"]/small[starts-with(text(),"m")]/../text()').extract().pop().replace(
    #             '.', '').strip()) if len(
    #         flat.xpath('span[@class="item-detail"]/small[starts-with(text(),"m")]')) == 1 else None for flat in
    #                 info_flats_xpath]
    #
    #     for flat in zip(links, prices, addresses, discounts, sqfts_m2, rooms):
    #         item = IdealistaItem(date=datetime.now().strftime('%Y-%m-%d'),
    #                              link=flat[0], price=flat[1], address=flat[2], discount=flat[3],
    #                              sqft_m2=flat[4], rooms=flat[5], baths=baths)
    #         yield item

    # Overriding parse_start_url to get the first page
    parse_start_url = parse_flat_list
