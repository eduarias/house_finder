from django_filters import FilterSet, RangeFilter, NumberFilter, CharFilter

from .models import House


class HouseFilter(FilterSet):
    price = RangeFilter(name='price')
    rooms = NumberFilter(name='rooms', label='Min. rooms', lookup_expr='gte')
    baths = NumberFilter(name='baths', label='Min. baths', lookup_expr='gte')
    description = CharFilter(name='description', label='Description', lookup_expr='icontains')

    class Meta:
        model = House
        fields = [
            'price',
            'rooms',
            'baths',
            'description'
        ]
