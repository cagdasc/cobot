# -*- coding: utf-8 -*-

# Scrapy settings for cobot project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'cobot'

SPIDER_MODULES = ['cobot.spiders']
NEWSPIDER_MODULE = 'cobot.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'cobot (+http://www.yourdomain.com)'
USER_AGENT = 'cobot is writing for final year project. It crawls and clusters downloaded page by structural similarity'
DOWNLOAD_DELAY = 0.5

ITEM_PIPELINES = {
    'cobot.pipelines.CobotPipeline': 20
}
