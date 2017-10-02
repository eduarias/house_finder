# -*- coding: utf-8 -*-

# Scrapy settings for home_crawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
import os
import sys
import django


BOT_NAME = 'house_crawler'

SPIDER_MODULES = ['house_crawler.spiders']
NEWSPIDER_MODULE = 'house_crawler.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'home_crawler (example@example.net)'
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
HTTPCACHE_ENABLED = False
AUTOTHROTTLE_ENABLED = True
ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {'house_crawler.pipelines.DjangoPipeline': 100,
                  }

LOG_STDOUT = True
LOG_ENABLED = True
LOG_FILE = '/tmp/scrapy_output.txt'

PWD = os.path.dirname(__file__)
DJANGO_PROJECT_PATH = os.path.join(PWD, '..', 'house_finder')
DJANGO_SETTINGS_MODULE = 'house_finder.settings'

sys.path.insert(0, DJANGO_PROJECT_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = DJANGO_SETTINGS_MODULE
django.setup()
