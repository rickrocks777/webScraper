import scrapy
from datetime import datetime
import re
from sqlalchemy import create_engine
from urllib.parse import quote
from sqlalchemy.orm import sessionmaker
from scriptRun import WebsiteScraped

db_username = "master"
db_password = "Aspl@345!"
db_host = "1.23.242.234"
db_port = '3306'
db_name = "gurugaon_sm_cid"

encoded_password = quote(db_password)


engine = create_engine(f"mysql+pymysql://{db_username}:{encoded_password}@{db_host}:{db_port}/{db_name}")
Session = sessionmaker(bind=engine)
session = Session()

def extractDates(html_content):
        try:
            date_pattern = r'>\s*(\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s\d{1,2},\s\d{4}\s\d{1,2}:\d{2}\s(?:am|pm))\s*<'

            match = re.search(date_pattern, html_content)

            if match:
                date_time = match.group(1)
                return date_time
            else:
                return None
        except:
            return None

class DynamicspiderSpider(scrapy.Spider):
    name = "dynamicSpider"

    def __init__(self, start_urls=None, allowed_domains=None, *args, **kwargs):
        super(DynamicspiderSpider, self).__init__(*args, **kwargs)
        self.start_urls = start_urls.split(',') if start_urls else []
        self.allowed_domains = allowed_domains.split(',') if allowed_domains else []

    def parse(self, response):
        today_date = datetime.today().strftime('%A, %B %d, %Y')
        
        date_divs = ["div.epaper-date::text","div.column p::text","div.date span::text","div.jsx-c1a6c01267c54545.sliderHd.text-center::text"]
        dates = []

        for date_div in date_divs:
            date_today = response.css(date_div).get()

            # Check if date_today is not None
            if date_today:
                date_today = date_today  # Clean up the date string
                dates.append(date_today)  # Add the date to the list
            else:
                dates.append(today_date)
                self.log(f"No date found for selector: {date_div}")

        existing_record = session.query(WebsiteScraped).filter(WebsiteScraped.url == response.url).first()
        url_id = existing_record.id if existing_record else None

        print(f"Parsing page: {response.url}")
        headings = response.css("a")
        for heading in headings:
            text = heading.css('::text').get()
            url = heading.css('::attr(href)').get()
            parent_div = heading.xpath("ancestor::div[1]").get()
            yield {
                'text': text,
                'url': response.urljoin(url),
                'publish_date': dates[0],
                'article_date': extractDates(parent_div),
                'website_Scrap_id':url_id
            }

        paragraphs = response.css("p")
        for para in paragraphs:
            text = para.css('::text').get()
            yield {
                'text': text,
                'url': response.url,
                'publish_date': dates[0],
                'website_Scrap_id':url_id
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
                    'publish_date': dates[0],
                    'website_Scrap_id':url_id
                }       
        next_page = response.css('a.next::attr(href)').get() 
        if next_page:
            next_page_url = response.urljoin(next_page)
            print(f"Next page URL: {next_page_url}")
            yield scrapy.Request(url=next_page_url, callback=self.parse)

