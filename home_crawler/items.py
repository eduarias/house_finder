# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HomeItem(scrapy.Item):
    #Matching variables of every flat to be scrapped
    title = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()
    address = scrapy.Field()
    sqft_m2 = scrapy.Field()
    rooms = scrapy.Field()
    baths = scrapy.Field()
    update_date = scrapy.Field()
    last_updated = scrapy.Field(serializer=str)


class IdealistaItem(HomeItem):
    id_idealista = scrapy.Field()


class FotocasaItem(HomeItem):
    id_fotocasa = scrapy.Field()


class HabitacliaItem(HomeItem):
    id_habitaclia = scrapy.Field()