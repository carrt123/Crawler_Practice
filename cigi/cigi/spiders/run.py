import os

import scrapy
from scrapy import Request
from ..items import CigiItem


class RunSpider(scrapy.Spider):
    name = "run"
    limit = 10
    offset = 0
    base_url = "https://www.cigionline.org"
    url = f"https://www.cigionline.org/api/search/?limit={limit}&offset=%s&sort=date&field=authors&field=publishing_date&publicationtypeid=89"
    base_folder = 'cigi_pdfs'

    def start_requests(self):
        if not os.path.exists(self.base_folder):
            os.makedirs(self.base_folder)
        yield Request(self.url % self.offset, callback=self.parse)

    def parse(self, response, **kwargs):
        data = response.json()
        items = data.get('items')
        for item in items:
            cigiItem = CigiItem()
            cigiItem['title'] = item.get('title')
            cigiItem['authors'] = [i['title'] for i in item.get('authors')]
            cigiItem['publishing_date'] = item.get('publishing_date')
            yield Request(self.base_url + item.get('url'), callback=self.parse_detail, meta={'cigiItem': cigiItem})
        self.offset += self.limit
        # if self.offset < data['meta'].get('total_count'):
        if self.offset < 20:
            yield Request(self.url % self.offset, callback=self.parse)

    def parse_detail(self, response):
        cigiItem = response.meta['cigiItem']
        cigiItem['abstract'] = response.css('.paragraph-block p::text').get()
        pdf_url = response.css('.social-share-list ~ a::attr(href)').get()
        cigiItem['pdf'] = pdf_url.split('/')[-1]
        yield cigiItem

        yield Request(self.base_url + pdf_url, callback=self.save_pdf)

    def save_pdf(self, response):
        name = response.url.split('/')[-1]
        file_path = os.path.join(self.base_folder, name)
        with open(file_path, 'wb') as f:
            f.write(response.body)
