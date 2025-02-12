import os
import sys

def scrapUrl(url):
    os.system(f'scrapy crawl dynamicSpider -a start_urls="{url}" -o output.json')

def clear_json_file(file_path):
    with open(file_path,'w') as file:
        pass


if __name__ == "__main__":
    url = sys.argv[1]
    clear_json_file('tutorial\output.json')
    scrapUrl(url)    

# scrapUrl("https://timesofindia.indiatimes.com/india/haryana")

