from django_filters import FilterSet

from .models import House


class HouseFilter(FilterSet):

    class Meta:
        model = House
        fields = {
            'price': ['gt', 'lt'],
            'rooms': ['gt'],
            'baths': ['gt'],
            'description': ['icontains']
        }
