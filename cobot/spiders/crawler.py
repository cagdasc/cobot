__author__ = 'cagdascaglak'

import os
from scrapy import log
from cobot.spiders import is_allowed, create_site_dir
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from cobot.items import CobotItem

from lxml import html
from bs4 import BeautifulSoup


class PageWalker(CrawlSpider):
    name = 'cobot'
    rules = (Rule(LxmlLinkExtractor(), callback='walker', follow=True),)

    def __init__(self, *args, **kwargs):
        super(PageWalker, self).__init__(*args, **kwargs)
        self.allowed_domains = kwargs.get('allowed').split(',')
        self.start_urls = kwargs.get('start').split(',')
        self.main_site = kwargs.get('main')
        self.page_dir = create_site_dir(self.main_site)

    def walker(self, response):
        page_items = CobotItem()

        try:
            file_name = response.url.split(self.allowed_domains[0])[1]
            file_name = ''.join(file_name.split('/'))

            form = response.xpath('//form').extract()
            if form:
                if is_allowed(file_name):
                    with open(os.path.join(self.page_dir, file_name), 'w') as f:
                        f.write(response.body)
                    page_items['page_url'] = response.url
                    page_items['page_name'] = file_name

        except IOError:
            pass

        return page_items