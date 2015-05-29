# Copyright 2015 Cagdas Caglak

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__author__ = 'cagdascaglak'

import os
import json
from collections import namedtuple
import cobot.settings
from cobot import config
from cobot.spiders import is_allowed, create_site_dir
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from cobot.items import CobotItem

from time import gmtime, strftime


class PageWalker(CrawlSpider):
    name = 'cobot'
    rules = (Rule(LxmlLinkExtractor(), callback='walker', follow=True),)

    def __init__(self, __config):
        super(PageWalker, self).__init__(__config)
        self.__config = __config
        self.allowed_domains = self.__config.initialize.allowed_domains
        self.start_urls = self.__config.initialize.start_urls
        self.main_site = self.__config.initialize.site_name + '_' + strftime('%Y%m%d-%H%M%S', gmtime())
        self.page_dir = create_site_dir(self.main_site)
        self.algorithm = self.__config.algorithm
        self.initialize = self.__config.initialize

        cobot.settings.ROBOTSTXT_OBEY = self.__config.cobot_settings.robots
        cobot.settings.CLOSESPIDER_PAGECOUNT = self.__config.cobot_settings.page_count

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
                    page_items['page_full_path'] = os.path.join(self.page_dir, file_name)

        except IOError:
            pass

        return page_items