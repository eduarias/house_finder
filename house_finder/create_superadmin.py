#!/usr/bin/env python

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'house_finder.settings'
import django
django.setup()
from django.contrib.auth.management.commands.createsuperuser import get_user_model
if get_user_model().objects.filter(username=os.environ['DJANGO_SU_USERNAME']): 
    print('Super user already exists. SKIPPING...')
else:
    print('Creating super user...')
    get_user_model()._default_manager.create_superuser(
    	username=os.environ['DJANGO_SU_USERNAME'], 
    	email=os.environ['DJANGO_SU_EMAIL'], 
    	password=os.environ['DJANGO_SU_PASSWORD'])
    print('Super user created...')