from datetime import timedelta

from django.utils import timezone

from django_filters import FilterSet, RangeFilter, \
    NumberFilter, CharFilter

from .models import House


class HouseFilter(FilterSet):
    price = RangeFilter(name='price')
    rooms = NumberFilter(name='rooms', label='Min. rooms', lookup_expr='gte')
    baths = NumberFilter(name='baths', label='Min. baths', lookup_expr='gte')
    description = CharFilter(name='description', label='Description', lookup_expr='icontains')
    last_days = NumberFilter(name='updated_at', label='Updated last days', method='found_last_days')

    class Meta:
        model = House
        fields = [
            'price',
            'rooms',
            'baths',
            'description',
            'last_days'
        ]

    @staticmethod
    def found_last_days(queryset, name, value):
        time_threshold = timezone.now() - timedelta(days=int(value))
        lookup = '__'.join([name, 'gte'])
        return queryset.filter(**{lookup: time_threshold})
