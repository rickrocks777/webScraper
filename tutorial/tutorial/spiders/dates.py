import scrapy
import re

class DatesSpider(scrapy.Spider):
    name = "dates"
    allowed_domains = ["indianexpress.com"]
    start_urls = ["https://indianexpress.com/about/haryana/"]
    
    # Updated regular expression to match full date formats, including optional year and time
    date_pattern = r"\b(January|February|March|April|May|June|July|August|September|October|November|December)\s([1-9]|[12][0-9]|30|31)(?:,?\s\d{4})?(?:\s\d{1,2}:\d{2}\s(?:am|pm))?\b"

    def parse(self, response):
        for a_tag in response.css('a'):
            # Get the parent div of the <a> tag
            parent_div = a_tag.xpath('ancestor::div[1]')

            # Extract all <p> tags inside the parent div and iterate through them
            for p_tag in parent_div.xpath('.//p'):
                # Extract the text from the <p> tag, including all text nodes
                p_text = ''.join(p_tag.xpath('.//text()').getall()).strip()

                # Debug: print the extracted p_text
                self.logger.info(f"Extracted p_text: '{p_text}'")

                # Search for a date in the <p> tag's text using regex
                if re.search(self.date_pattern, p_text):
                    # If a date is found, yield the <a> tag, the date, and the <p> text
                    yield {
                        'date_in_p_tag': True,
                        'date_text': p_text,
                    }
                    break  # Stop checking other <p> tags once a date is found

