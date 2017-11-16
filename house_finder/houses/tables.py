import django_tables2 as tables
from django_tables2.utils import A
from .models import House


class HouseTable(tables.Table):
    title = tables.LinkColumn(accessor='houses:detail', args=[A('pk')], attrs={'th': {'id': 'header-title'}})
    url = tables.TemplateColumn('<a href="{{ record.url }}">{{ record.provider }}</a>',
                                order_by='start_url.provider.name',
                                attrs={'th': {'id': 'header-url'}})
    neighborhood = tables.Column('neighborhood',
                                 A('start_url.neighborhood'),
                                 attrs={'th': {'id': 'header-neighborhood'}})
    price = tables.Column(accessor='price', attrs={'th': {'id': 'header-price'}})
    sqft_m2 = tables.Column(accessor='sqft_m2', verbose_name='m2', attrs={'th': {'id': 'header-sqft_m2'}})
    rooms = tables.Column(accessor='rooms', attrs={'th': {'id': 'header-rooms'}})
    baths = tables.Column(accessor='baths', attrs={'th': {'id': 'header-baths'}})

    class Meta:
        model = House
        fields = ('title', 'neighborhood',
                  'price', 'sqft_m2',
                  'rooms', 'baths', 'url',
                  )
        attrs = {"class": "table-striped table-bordered"}
        empty_text = "There are no houses matching the search criteria..."
