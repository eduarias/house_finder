from django.contrib import admin

from .models import House, StartURL, HousesProvider, City, District, Neighborhood

house_models = [House, StartURL, HousesProvider, City, District, Neighborhood]
admin.site.register(house_models)
