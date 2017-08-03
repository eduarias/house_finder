import django_tables2 as tables
from django_tables2.utils import A
from .models import House


class HouseTable(tables.Table):
    title = tables.LinkColumn('houses:detail', args=[A('pk')])
    # neighborhood = tables.LinkColumn('houses:detail', args=[A('pk')])
    # price = tables.LinkColumn('houses:detail', args=[A('pk')])
    # rooms = tables.LinkColumn('houses:detail', args=[A('pk')])

    class Meta:
        model = House
        fields = ('title', 'neighborhood',
                  'price', 'sqft_m2',
                  'rooms',)
        attrs = {"class": "table-striped table-bordered"}
        empty_text = "There are no customers matching the search criteria..."