"""
Tables can be created from a range of input data structures. If you have seen the tutorial
you will have seen a QuerySet being used, however any iterable that supports len() and contains
items that exposes key-based access to column values is fine.
"""
import django_tables2 as tables
from django_tables2.utils import A
from .models import House


class HouseTable(tables.Table):
    """Definition of the table to show houses"""
    title = tables.LinkColumn('houses:detail', args=[A('pk')])
    url = tables.TemplateColumn('<a href="{{ record.url }}">{{ record.provider }}</a>',
                                order_by='start_url.provider.name')
    neighborhood = tables.Column('neighborhood', A('start_url.neighborhood'))

    class Meta:
        """Define the model and fields used to show in the table"""
        model = House
        fields = ('title', 'neighborhood',
                  'price', 'sqft_m2',
                  'rooms', 'baths', 'url',
                  )
        attrs = {"class": "table-striped table-bordered"}
        empty_text = "There are no houses matching the search criteria..."
