import scrapy
from scrapy.crawler import CrawlerProcess
from tutorial.spiders.webList import WeblistSpider
from tutorial.spiders.indianExpress import IndianexpressSpider 

process = CrawlerProcess(
    settings={
        'FEED_FORMAT': 'json',  # Output format
        'FEED_URI': 'output.json'
    }
)

process.crawl(WeblistSpider)
process.crawl(IndianexpressSpider)
process.start()