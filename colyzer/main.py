__author__ = 'cagdascaglak'

import sys
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from cobot.spiders.crawler import PageWalker
from scrapy.utils.project import get_project_settings

if __name__ == '__main__':
    spider = PageWalker(cfg=sys.argv[1])
    settings = get_project_settings()
    crawler = Crawler(settings)
    crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()
    log.start(loglevel=log.INFO)
    log.start_from_crawler(crawler)
    reactor.run()