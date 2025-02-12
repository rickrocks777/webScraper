import scrapy
from datetime import datetime
import re

def extractDates(html_content):
        date_pattern = r'>\s*(\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s\d{1,2},\s\d{4}\s\d{1,2}:\d{2}\s(?:am|pm))\s*<'

        # Search for the pattern in the HTML content
        match = re.search(date_pattern, html_content)

        if match:
            date_time = match.group(1)
            return date_time
        else:
            return None

class DynamicspiderSpider(scrapy.Spider):
    name = "dynamicSpider"

    def __init__(self, start_urls=None, allowed_domains=None, *args, **kwargs):
        super(DynamicspiderSpider, self).__init__(*args, **kwargs)
        self.start_urls = start_urls.split(',') if start_urls else []
        self.allowed_domains = allowed_domains.split(',') if allowed_domains else []

    def parse(self, response):
        today_date = datetime.today().strftime('%A, %B %d, %Y')
        print(f"Parsing page: {response.url}")
        headings = response.css("a")
        for heading in headings:
            text = heading.css('::text').get()
            url = heading.css('::attr(href)').get()
            parent_div = heading.xpath("ancestor::div[1]").get()
            yield {
                'text': text,
                'url': response.urljoin(url),
                'publish_date': today_date,
                'parent-div': extractDates(parent_div)
            }

        paragraphs = response.css("p")
        for para in paragraphs:
            text = para.css('::text').get()
            yield {
                'text': text,
                'url': response.url,
                'publish_date': today_date
            }

        
        # links = response.css('a::attr(href)').getall()
        # for link in links:
        #     full_url = response.urljoin(link)
        #     yield {
        #         'link': full_url,
        #         'url': response.url
        #     }

        lists = response.css('ul')
        for list in lists:
            list_items = list.css('li')
            list_item_link = list.css('li a::text')
            for list_item in list_items:
                yield {
                    "text":list_item.css('::text').get(),
                    "url" : response.urljoin(list_item_link.get()),
                    'publish_date': today_date
                }       
        next_page = response.css('a.next::attr(href)').get() 
        if next_page:
            next_page_url = response.urljoin(next_page)
            print(f"Next page URL: {next_page_url}")
            yield scrapy.Request(url=next_page_url, callback=self.parse)

