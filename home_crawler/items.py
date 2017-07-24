from scrapy_djangoitem import DjangoItem
from store_houses.models import Home


class HomeItem(DjangoItem):
    django_model = Home
