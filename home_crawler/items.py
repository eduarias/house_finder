# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HomeItem(scrapy.Item):
    #Matching variables of every flat to be scrapped
    id_idealista = scrapy.Field()
    update_date = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field()
    address = scrapy.Field()
    sqft_m2 = scrapy.Field()
    rooms = scrapy.Field()
    baths = scrapy.Field()
    discount = scrapy.Field()
    last_updated = scrapy.Field(serializer=str)

