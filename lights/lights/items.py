# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LightsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    final_price = scrapy.Field()
    model_number = scrapy.Field()
    menards_sku = scrapy.Field()
    features = scrapy.Field()
    brand = scrapy.Field()


