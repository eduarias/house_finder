# -*- coding: utf-8 -*-

# Scrapy settings for home_crawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'home_crawler'

SPIDER_MODULES = ['home_crawler.spiders']
NEWSPIDER_MODULE = 'home_crawler.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'home_crawler (+http://www.yourdomain.com)'
USER_AGENT = "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36"
DOWNLOAD_DELAY = 0.5


ITEM_PIPELINES = {'home_crawler.pipelines.MongoDBPipeline': 100,
                  }

MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "homes"
MONGODB_COLLECTION = "home"