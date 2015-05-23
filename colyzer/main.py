__author__ = 'cagdascaglak'

import os
from lxml import etree
from colyzer import ShingleBased, SelkowTED, ClusterAlgorithms
from cobot.spiders import SITES
import json
from collections import namedtuple

import sys
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from cobot.spiders.crawler import PageWalker
from scrapy.utils.project import get_project_settings

if __name__ == '__main__':
    debug_mode = 1
    if debug_mode == 0:
        spider = PageWalker(cfg=sys.argv[1])
        settings = get_project_settings()
        crawler = Crawler(settings)
        crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
        crawler.configure()
        crawler.crawl(spider)
        crawler.start()
        log.start_from_crawler(crawler)
        reactor.run()
    else:
        with open(sys.argv[1]) as f:
            config_file = f.read()
            print(config_file)
            __config = json.loads(config_file, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
        algorithm = __config.algorithm.which

        doc_list = []
        html_files_path = []
        for top_dir0, sub_dirs0, files0 in os.walk(os.path.join(SITES)):
            for site_dir in sub_dirs0:
                for top_dir1, sub_dirs1, page_files in os.walk(os.path.join(top_dir0, site_dir)):
                    for html_file in page_files:
                        print(os.path.join(top_dir1, html_file))
                        tree = etree.parse(os.path.join(top_dir1, html_file),
                                           parser=etree.HTMLParser(remove_comments=True))

                        root_tag = tree.getroot()[1]

                        if algorithm == 'shingle':
                            doc = ShingleBased.Document(html_file)
                            doc.find_all_real_paths(root_tag, -1)
                            doc.find_all_virtual_paths(root_tag, 0)
                            doc_list.append(doc)
                        else:
                            doc = SelkowTED.Nodes(root_tag, doc_name=html_file)
                            doc_list.append(doc)

        if algorithm == 'shingle':
            distance_matrix = ShingleBased.get_distance_matrix(doc_list)
            print(distance_matrix)
            clustering = ClusterAlgorithms.Clustering(__config.algorithm.shingle.threshold,
                                                      __config.algorithm.shingle.iteration,
                                                      __config.algorithm.shingle.cluster_size,
                                                      __config.initialize.site_name)
            clustering.process(doc_list, distance_matrix)
            clustering.pretty_print()
        else:
            distance_matrix = SelkowTED.get_distance_matrix(doc_list)
            print(distance_matrix)
            clustering = ClusterAlgorithms.Clustering(__config.algorithm.ted.threshold,
                                                      __config.algorithm.ted.iteration,
                                                      __config.algorithm.ted.cluster_size,
                                                      __config.initialize.site_name)
            clustering.process(doc_list, distance_matrix)
            clustering.pretty_print()