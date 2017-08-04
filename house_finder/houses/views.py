from django.views import generic
from django_tables2 import RequestConfig

from .models import House
from .tables import HouseTable


class HousesListView(generic.ListView):
    model = House
    template_name = 'houses/houses_list2.html'
    context_object_name = 'houses'
    ordering = ['price']

    def get_context_data(self, **kwargs):
        context = super(HousesListView, self).get_context_data(**kwargs)
        # context['nav_customer'] = True
        table = HouseTable(House.objects.order_by('price'))
        RequestConfig(self.request, paginate={'per_page': 20}).configure(table)
        context['table'] = table
        return context


class DetailView(generic.DetailView):
    model = House
    template_name = 'houses/detail.html'
