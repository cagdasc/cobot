# -*- coding: utf-8 -*-

# Scrapy settings for cobot project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
# http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'cobot'

SPIDER_MODULES = ['cobot.spiders']
NEWSPIDER_MODULE = 'cobot.spiders'

USER_AGENT = 'cobot is writing for final year project. It crawls and clusters downloaded page by structural similarity'
DOWNLOAD_DELAY = 0.5

"""
ITEM_PIPELINES = {
    'cobot.pipelines.CobotPipeline': 20
}
"""

ITEM_PIPELINES = ['cobot.pipelines.CobotPipeline']

ROBOTSTXT_OBEY = True

CLOSESPIDER_PAGECOUNT = 5

EXTENSIONS = {}

EXTENSIONS_BASE = {
    'scrapy.contrib.closespider.CloseSpider': 0,
}