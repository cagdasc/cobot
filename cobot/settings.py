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

BOT_NAME = 'cobot'

SPIDER_MODULES = ['cobot.spiders']
NEWSPIDER_MODULE = 'cobot.spiders'

USER_AGENT = 'cobot is writing for final year project. It crawls and clusters downloaded page by structural similarity'
DOWNLOAD_DELAY = 0.5

ITEM_PIPELINES = {
    'cobot.pipelines.CobotPipeline': 20
}
"""
ITEM_PIPELINES = ['cobot.pipelines.CobotPipeline']
"""

ROBOTSTXT_OBEY = True

CLOSESPIDER_PAGECOUNT = 5

EXTENSIONS = {}

EXTENSIONS_BASE = {
    'scrapy.contrib.closespider.CloseSpider': 0,
}