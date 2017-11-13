from django.views import generic
from django_filters.views import FilterView
from django_tables2 import SingleTableView

from .models import House
from .tables import HouseTable
from .filters import HouseFilter


class HousesListView(FilterView, SingleTableView):
    model = House
    template_name = 'houses/houses_list.html'
    context_object_name = 'houses'
    ordering = ['price']
    filterset_class = HouseFilter
    table_class = HouseTable


class DetailView(generic.DetailView):
    model = House
    template_name = 'houses/detail.html'
    model.has_seen = True
