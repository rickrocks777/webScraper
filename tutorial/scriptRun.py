import os
import sys

def scrapUrl(url):
    os.system(f'scrapy crawl dynamicSpider -a start_urls="{url}" -o output.json')

if __name__ == "__main__":
    url = sys.argv[1]
    scrapUrl(url)    

# scrapUrl("https://timesofindia.indiatimes.com/india/haryana")

