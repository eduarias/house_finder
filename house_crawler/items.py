from scrapy_djangoitem import DjangoItem
from store_houses.models import House


class HouseItem(DjangoItem):
    django_model = House
