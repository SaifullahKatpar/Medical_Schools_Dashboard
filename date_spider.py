import scrapy
from scrapy.linkextractors import LinkExtractor
from fuzzywuzzy import fuzz
import re
from bs4 import BeautifulSoup
from dateutil.parser import parse
import datetime

class DateSpider(scrapy.Spider):
    name = 'date_spider'
    allowed_domains = ['hofstra.edu']
    start_urls = ['https://www.hofstra.edu/admission/apply.html']
    seen_dates = set()

    def __init__(self, *args, **kwargs):
        super(DateSpider, self).__init__(*args, **kwargs)
        self.link_extractor = LinkExtractor(
            allow_domains=self.allowed_domains,
            allow=r'admission|application'
        )

    def parse(self, response):
        # Define a regular expression pattern to match dates in various formats.
        date_pattern = r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\b(?:[ ./-]*\d{1,2}[ ./-]*(?:\d{2,4})?)?'        # Extract the HTML content from the response.
        html = response.body

        # Use a regular expression to find all matches of the pattern in the HTML string.
        matches = re.findall(date_pattern, html.decode('utf-8'))
        new_dates = set(matches) - self.seen_dates

        for date in new_dates:
            self.seen_dates.add(date)
            yield {
                'date': date,
                'url': response.url,
            }


        # Return a list of unique matches.
        dates = list(set(matches))
        yield {'dates': dates}
        if len(self.seen_dates) < 10:            
            for link in self.link_extractor.extract_links(response):
                yield scrapy.Request(link.url, callback=self.parse)
