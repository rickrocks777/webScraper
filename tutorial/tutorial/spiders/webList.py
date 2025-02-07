import scrapy

class WeblistSpider(scrapy.Spider):
    name = "webList"
    allowed_domains = ["www.tribuneindia.com", "timesofindia.indiatimes.com"]
    start_urls = ["https://www.tribuneindia.com/news/state/haryana",
                  "https://timesofindia.indiatimes.com/india/haryana"]

    def parse(self, response):
        print(f"Parsing page: {response.url}")

        # Extracting h2 titles
        h2_titles = response.css("div.h2-title")
        for h2_title in h2_titles:
            a_tag = h2_title.css('h2 a')
            href = a_tag.css('::attr(href)').get()  # Extract href attribute
            text = a_tag.css('::text').get()
            yield {
                "text": text,
                "url": response.urljoin(href)
            }

        # Extracting span titles
        span_tiles = response.css("span.w_tle a")
        for span_tile in span_tiles:
            text = span_tile.css('::text').get()
            text = text.replace("\n", "")
            url = span_tile.css('::attr(href)').get()
            yield {
                "text": text,
                "url": response.urljoin(url)
            }

        # Extracting tab content
        tabContent = response.css("div.tab-content")
        for div in tabContent:
            ul_tags = div.css('ul')
            for ul_tag in ul_tags:
                li_tags = ul_tag.css('li')
                for li_tag in li_tags:
                    a_tag = li_tag.css('a')
                    text = a_tag.css('::text').get()
                    url = a_tag.css('::attr(href)').get()
                    yield {
                        "text": text,
                        "url":response.urljoin(url)
                    }

        # Debug: Print pagination URLs
        next_pages = response.css('ul.curpgcss li a::attr(href)').getall()
        print(f"Pagination links found: {next_pages}")  # Debugging pagination

        # Pagination handling
        for next_page in next_pages:
            if next_page:
                next_page_url = response.urljoin(next_page)
                print(f"Next page URL: {next_page_url}")
                yield scrapy.Request(url=next_page_url, callback=self.parse)


    # Optional: custom callback to re-use the parse method for next page
    # def parse_next_page(self, response):
    #     print(f"Parsing next page: {response.url}")
    #     yield from self.parse(response)

