# items.py

import scrapy


class ChocolateProduct(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    price = scrapy.Field()
    # add other fields as necessary
