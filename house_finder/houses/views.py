from django.views import generic
from django_tables2 import RequestConfig, SingleTableView

from .models import House
from .tables import HouseTable
from .filters import HouseFilter


class FilteredSingleTableView(SingleTableView):
    filter_class = None

    def get_table_data(self):
        data = super(FilteredSingleTableView, self).get_table_data()
        self.filter = self.filter_class(self.request.GET, queryset=data)
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super(FilteredSingleTableView, self).get_context_data(**kwargs)
        context['filter'] = self.filter
        return context


class HousesListView(FilteredSingleTableView):
    model = House
    template_name = 'houses/houses_list2.html'
    context_object_name = 'houses'
    ordering = ['price']
    filter_class = HouseFilter
    table_class = HouseTable

    def get_context_data(self, **kwargs):
        context = super(HousesListView, self).get_context_data(**kwargs)
        context['nav_customer'] = True
        table = HouseTable(House.objects.order_by('price'))
        RequestConfig(self.request, paginate={'per_page': 20}).configure(table)
        context['table'] = table
        return context


class DetailView(generic.DetailView):
    model = House
    template_name = 'houses/detail.html'
    model.has_seen = True
