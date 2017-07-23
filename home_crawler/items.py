from scrapy_djangoitem import DjangoItem
from store_houses.models import Home

import scrapy


class HomeItem(DjangoItem):
    django_model = Home


class IdealistaItem(HomeItem):
    id_idealista = scrapy.Field()


class FotocasaItem(HomeItem):
    id_fotocasa = scrapy.Field()


class HabitacliaItem(HomeItem):
    id_habitaclia = scrapy.Field()