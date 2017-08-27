from scrapy_djangoitem import DjangoItem
from houses.models import House


class HouseItem(DjangoItem):
    django_model = House
