import scrapy


class DynamicspiderSpider(scrapy.Spider):
    name = "dynamicSpider"

    def __init__(self, start_urls=None, allowed_domains=None, *args, **kwargs):
        super(DynamicspiderSpider, self).__init__(*args, **kwargs)
        self.start_urls = start_urls.split(',') if start_urls else []
        self.allowed_domains = allowed_domains.split(',') if allowed_domains else []

    def parse(self, response):
        # You can add dynamic selectors for different website elements here
        print(f"Parsing page: {response.url}")

        # Example of dynamic CSS selectors for headlines, links, etc.
        # You can pass this through arguments or handle via settings/configurations.

        # For example, extracting headings
        headings = response.css("h1, h2, h3, h4, h5, h6")
        for heading in headings:
            text = heading.css('::text').get()
            yield {
                'heading_text': text,
                'url': response.url
            }

        # You can add more dynamic sections like paragraphs, articles, etc.
        paragraphs = response.css("p")
        for para in paragraphs:
            text = para.css('::text').get()
            yield {
                'paragraph_text': text,
                'url': response.url
            }

        # Extracting links dynamically
        links = response.css('a::attr(href)').getall()
        for link in links:
            full_url = response.urljoin(link)
            yield {
                'link': full_url,
                'url': response.url
            }

        # Pagination handling
        next_page = response.css('a.next::attr(href)').get()  # Adjust for specific pagination
        if next_page:
            next_page_url = response.urljoin(next_page)
            print(f"Next page URL: {next_page_url}")
            yield scrapy.Request(url=next_page_url, callback=self.parse)
