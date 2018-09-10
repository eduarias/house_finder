from scrapy_djangoitem import DjangoItem
from houses.models import House


class HouseItem(DjangoItem):
    """House definition is handle by Django model"""
    django_model = House
