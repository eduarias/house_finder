"""
A view function, or view for short, is simply a Python function that takes a Web request
and returns a Web response.
This response can be the HTML contents of a Web page, or a redirect, or a 404 error, or an
XML document, or an image . . . or anything, really. The view itself contains whatever
arbitrary logic is necessary to return that response.
"""
from django.views import generic
from django_filters.views import FilterView
from django_tables2 import SingleTableView

from .models import House
from .tables import HouseTable
from .filters import HouseFilter


class HousesListView(FilterView, SingleTableView):
    """View for a list of houses with filtering"""
    model = House
    template_name = 'houses/houses_list2.html'
    context_object_name = 'houses'
    ordering = ['price']
    filterset_class = HouseFilter
    table_class = HouseTable

    def get_context_data(self, **kwargs):
        """Filter the base data to be shown"""
        context = super(HousesListView, self).get_context_data(**kwargs)
        context['rent'] = House.objects.filter(start_url__type__exact='R')
        return context


class DetailView(generic.DetailView):
    """View of the details of a house"""
    model = House
    template_name = 'houses/detail.html'
    model.has_seen = True
