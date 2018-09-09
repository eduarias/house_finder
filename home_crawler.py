from time import sleep
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

#sleep(8)

process = CrawlerProcess(get_project_settings())

#process.crawl('idealista')
process.crawl('fotocasa')
process.crawl('habitaclia')
process.start()
