from django.contrib import admin

from .models import House, StartURL, HousesProvider

house_models = [House, StartURL, HousesProvider]
admin.site.register(house_models)
