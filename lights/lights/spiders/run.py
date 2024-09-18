from typing import Iterable

import scrapy
from scrapy import Request
from ..items import LightsItem


class RunSpider(scrapy.Spider):
    name = "run"
    page = 1
    url = "https://www.menards.com/main/lighting-ceiling-fans/indoor-lighting/island-lights/c-1445422076756.htm?queryType=storeItems&page=%s"
    base_url = "https://www.menards.com"

    def start_requests(self):
        yield Request(self.url % self.page, callback=self.parse)

    def parse(self, response, **kwargs):
        total_item = response.css('#searchTitle span::text').get()
        items = response.css('.details > a::attr(href)').getall()
        print(total_item)
        for item in items[:2]:
            print(self.base_url + item)
            yield Request(self.base_url + item, callback=self.detail)

        # self.page += 1
        # if self.page * 36 <= int(total_item):
        #     yield Request(self.url % self.page, callback=self.parse)

    def detail(self, response):
        item = LightsItem()
        item['title'] = response.css('.d-md-none > h1::text').get()
        item['final_price'] = response.css('.#itemFinalPrice::text').get()
        item['model_number'] = response.xpath('//*[@id="itemDetailPage"]/div/div/span[1]/span/text()').get()
        item["menards_sku"] = response.xpath('//*[@id="itemDetailPage"]/div/div/span[2]/span/text()').get()
        item['brand'] = response.xpath('//*[@id="itemTabs"]/div[3]/div[1]/div[2]/div[2]/div[2]/p/span/text()').get()
        item['features'] = response.xpath('//*[@id="features"]/div/ul/li/text()').getall()
        yield item
