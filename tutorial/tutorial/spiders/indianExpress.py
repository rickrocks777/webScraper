import scrapy


class IndianexpressSpider(scrapy.Spider):
    name = "indianExpress"
    allowed_domains = ["indianexpress.com"]
    start_urls = ["https://indianexpress.com/about/haryana/"]

    def parse(self, response):
        h3_tags = response.css('h3')
        for h3_tag in h3_tags:
            text = h3_tag.css('::text')
            url = h3_tag.css('::attr(href)')
            yield {
                "text": text.get(),
                "url": url.get()
            }
