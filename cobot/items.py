# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CobotItem(scrapy.Item):
    page_name = scrapy.Field()
    page_url = scrapy.Field()
    page_body = scrapy.Field()
