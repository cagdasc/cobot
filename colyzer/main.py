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

    with open(sys.argv[1]) as f:
        config_file = f.read()
        print(config_file)
        __config = json.loads(config_file, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

    if __config.crawling:
        spider = PageWalker(__config)
        settings = get_project_settings()
        crawler = Crawler(settings)
        crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
        crawler.configure()
        crawler.crawl(spider)
        crawler.start()
        log.start_from_crawler(crawler)
        reactor.run()
    else:
        algorithm = __config.algorithm.which

        doc_list = []
        """
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
                        elif algorithm == 'ted':
                            doc = SelkowTED.Nodes(root_tag, doc_name=html_file)
                            doc_list.append(doc)
                        else:
                            print('There is no algorithm!!')
        """
        print(os.path.join(SITES, __config.initialize.site_name))

        with open(os.path.join(SITES, __config.initialize.site_name + '_raw.json')) as f:
            doc_file = f.read()
            raw_docs_obj = json.loads(doc_file, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

        for top_dir, sub_dir_, page_files in os.walk(os.path.join(SITES, __config.initialize.site_name)):
            for html_file in page_files:
                print(os.path.join(os.path.join(SITES, __config.initialize.site_name), html_file))
                tree = etree.parse(os.path.join(os.path.join(SITES, __config.initialize.site_name), html_file),
                                   parser=etree.HTMLParser(remove_comments=True))

                i = 0
                while i < len(raw_docs_obj.raw_doc_list):
                    if html_file == raw_docs_obj.raw_doc_list[i].doc_name:
                        doc_link = raw_docs_obj.raw_doc_list[i].doc_link
                        i = len(raw_docs_obj.raw_doc_list)
                    i += 1

                root_tag = tree.getroot()[1]

                if algorithm == 'shingle':
                    doc = ShingleBased.Document(html_file, doc_link=doc_link)
                    doc.find_all_real_paths(root_tag, -1)
                    doc.find_all_virtual_paths(root_tag, 0)
                    doc_list.append(doc)
                elif algorithm == 'ted':
                    doc = SelkowTED.Nodes(root_tag, doc_name=html_file, doc_link=doc_link)
                    doc_list.append(doc)
                else:
                    print('There is no algorithm!!')

        if algorithm == 'shingle':
            distance_matrix = ShingleBased.get_distance_matrix(doc_list)
            print(distance_matrix)
        elif algorithm == 'ted':
            distance_matrix = SelkowTED.get_distance_matrix(doc_list)
            print(distance_matrix)
        else:
            print('There is no algorithm!!')

        if __config.algorithm.which_clustering == 'k_means':
            clustering = ClusterAlgorithms.Clustering(None,
                                                      __config.algorithm.k_means.iteration,
                                                      __config.algorithm.k_means.cluster_size,
                                                      __config.initialize.site_name)
            clustering.k_means_process(doc_list, distance_matrix)
        elif __config.algorithm.which_clustering == 'shingle_based':
            clustering = ClusterAlgorithms.Clustering(__config.algorithm.shingle_based.threshold,
                                                      __config.algorithm.shingle_based.iteration,
                                                      __config.algorithm.shingle_based.cluster_size,
                                                      __config.initialize.site_name)
            # clustering.process(doc_list, distance_matrix)
            clustering.process(doc_list, distance_matrix)
        else:
            print('There is no clustering algorithm!!')
        clustering.pretty_print()

