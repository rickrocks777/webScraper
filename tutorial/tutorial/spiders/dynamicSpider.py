import scrapy


class DynamicspiderSpider(scrapy.Spider):
    name = "dynamicSpider"

    def __init__(self, start_urls=None, allowed_domains=None, *args, **kwargs):
        super(DynamicspiderSpider, self).__init__(*args, **kwargs)
        self.start_urls = start_urls.split(',') if start_urls else []
        self.allowed_domains = allowed_domains.split(',') if allowed_domains else []

    def parse(self, response):
        print(f"Parsing page: {response.url}")
        headings = response.css("h1, h2, h3, h4, h5, h6")
        for heading in headings:
            text = heading.css('::text').get()
            yield {
                'heading_text': text,
                'url': response.url
            }

        paragraphs = response.css("p")
        for para in paragraphs:
            text = para.css('::text').get()
            yield {
                'paragraph_text': text,
                'url': response.url
            }

        links = response.css('a::attr(href)').getall()
        for link in links:
            full_url = response.urljoin(link)
            yield {
                'link': full_url,
                'url': response.url
            }

        lists = response.css('ul')
        for list in lists:
            list_items = list.css('li')
            for list_item in list_items:
                yield {
                    "list_item":list_item.css('::text').get()
                }
        next_page = response.css('a.next::attr(href)').get() 
        if next_page:
            next_page_url = response.urljoin(next_page)
            print(f"Next page URL: {next_page_url}")
            yield scrapy.Request(url=next_page_url, callback=self.parse)
