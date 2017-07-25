from django.views import generic

from .models import House


class IndexView(generic.ListView):
    template_name = 'houses/index.html'
    context_object_name = 'cheapest_houses_list'

    def get_queryset(self):
        """Return the cheapest five houses."""
        return House.objects.order_by('price')[:5]


class DetailView(generic.DetailView):
    model = House
    template_name = 'houses/detail.html'
