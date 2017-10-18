import django_tables2 as tables
from django_tables2.utils import A
from .models import House


class HouseTable(tables.Table):
    title = tables.LinkColumn('houses:detail', args=[A('pk')])
    url = tables.TemplateColumn('<a href="{{ record.url }}">{{ record.provider }}</a>',
                                order_by='start_url.provider.name')
    neighborhood = tables.Column('neighborhood', A('start_url.neighborhood'))

    class Meta:
        model = House
        fields = ('title', 'neighborhood',
                  'price', 'sqft_m2',
                  'rooms', 'baths', 'url',
                  )
        attrs = {"class": "table-striped table-bordered"}
        empty_text = "There are no houses matching the search criteria..."
