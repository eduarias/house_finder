from django.conf.urls import url

from . import views

app_name = 'houses'

urlpatterns = [
    url(r'^$', views.HousesListView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/detail', views.DetailView.as_view(), name='detail'),
]
