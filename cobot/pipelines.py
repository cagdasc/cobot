# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from lxml import etree
from colyzer import ShingleBased, SelkowTED, ClusterAlgorithms


class CobotPipeline(object):
    def __init__(self):
        self.doc_list = []
        self.ted_dist = []

    def open_spider(self, spider):
        print('OPENED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!111111')
        print('Algorithm -->>' + spider.algorithm.which)

    def process_item(self, item, spider):
        print('page name -->' + item['page_name'])
        print('Processing....')
        self.__create_doc_list(item, spider.algorithm.which)
        return item

    def close_spider(self, spider):
        print('CLOSED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1111111111')
        if spider.algorithm.which == 'shingle':
            distance_matrix = ShingleBased.get_distance_matrix(self.doc_list)
            print(distance_matrix)
            # clustering = ClusterAlgorithms.Clustering(0.755, 500, 5)
            clustering = ClusterAlgorithms.Clustering(spider.algorithm.shingle.threshold,
                                                      spider.algorithm.shingle.iteration,
                                                      spider.algorithm.shingle.cluster_size,
                                                      spider.initialize.site_name)
            clustering.process(self.doc_list, distance_matrix)
            clustering.pretty_print()
        elif spider.algorithm.which == 'ted':
            distance_matrix = SelkowTED.get_distance_matrix(self.doc_list)
            print(distance_matrix)
            # clustering = ClusterAlgorithms.Clustering(0.755, 500, 5)
            clustering = ClusterAlgorithms.Clustering(spider.algorithm.ted.threshold, spider.algorithm.ted.iteration,
                                                      spider.algorithm.ted.cluster_size, spider.initialize.site_name)
            clustering.process(self.doc_list, distance_matrix)
            clustering.pretty_print()

    def __create_doc_list(self, item, which):
        tree = etree.parse(item['page_full_path'], parser=etree.HTMLParser(remove_comments=True))
        root_tag = tree.getroot()[1]
        if which == 'shingle':
            doc = ShingleBased.Document(doc_name=item['page_name'], doc_link=item['page_url'])
            doc.find_all_real_paths(root_tag, -1)
            doc.find_all_virtual_paths(root_tag, 0)
            self.doc_list.append(doc)
        elif which == 'ted':
            doc = SelkowTED.Nodes(root_tag, doc_name=item['page_name'], doc_link=item['page_url'])
            self.doc_list.append(doc)