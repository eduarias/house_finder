"""
To design URLs for an app, you create a Python module informally called a URLconf (URL configuration).
This module is pure Python code and is a mapping between URL path expressions to Python functions
(your views).

This mapping can be as short or as long as needed. It can reference other mappings. And, because
it’s pure Python code, it can be constructed dynamically.
"""
from django.conf.urls import url

from . import views

app_name = 'houses'

urlpatterns = [
    url(r'^$', views.HousesListView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/detail', views.DetailView.as_view(), name='detail'),
]
