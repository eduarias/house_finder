import django_tables2 as tables
from django_tables2.utils import A
from .models import House


class HouseTable(tables.Table):
    title = tables.LinkColumn('houses:detail', args=[A('pk')])
    url = tables.URLColumn(text=lambda record: record.website)
    has_seen = tables.BooleanColumn()

    class Meta:
        model = House
        fields = ('title', 'neighborhood',
                  'price', 'sqft_m2',
                  'rooms', 'url', 'has_seen',
                  'is_interesting', 'is_discard')
        attrs = {"class": "table-striped table-bordered"}
        empty_text = "There are no customers matching the search criteria..."