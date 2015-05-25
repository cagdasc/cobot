# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from lxml import etree
from colyzer import ShingleBased, SelkowTED, ClusterAlgorithms
import json
import os
from cobot.spiders import SITES
from cobot import RawDocuments

class CobotPipeline(object):
    def __init__(self):
        self.doc_list = []

    def open_spider(self, spider):
        print('SPIDER OPENED!!')
        print('Algorithm -->>' + spider.algorithm.which)

    def process_item(self, item, spider):
        print('page name -->' + item['page_name'])
        self.__create_doc_list(item, spider.algorithm.which)
        return item

    def close_spider(self, spider):
        print('SPIDER CLOSED!!')
        raw_doc_list = []
        for doc in self.doc_list:
            raw_doc = ClusterAlgorithms.Document(doc.doc_name, doc.doc_link)
            raw_doc_list.append(raw_doc.__dict__)
        result = RawDocuments(raw_doc_list)

        json_txt = json.dumps(result.__dict__)
        with open(os.path.join(SITES, spider.initialize.site_name + '_raw.json'), 'w') as f:
            f.write(json_txt)

        if spider.algorithm.which == 'shingle':
            distance_matrix = ShingleBased.get_distance_matrix(self.doc_list)
            print(distance_matrix)
        elif spider.algorithm.which == 'ted':
            distance_matrix = SelkowTED.get_distance_matrix(self.doc_list)
            print(distance_matrix)
        else:
            print('There is no algorithm!!')
            return

        if spider.algorithm.which_clustering == 'k_means':
            clustering = ClusterAlgorithms.Clustering(None,
                                                      spider.algorithm.k_means.iteration,
                                                      spider.algorithm.k_means.cluster_size,
                                                      spider.initialize.site_name)
            clustering.k_means_process(self.doc_list, distance_matrix)
        elif spider.algorithm.which_clustering == 'shingle_based':
            clustering = ClusterAlgorithms.Clustering(spider.algorithm.shingle_based.threshold,
                                                      spider.algorithm.shingle_based.iteration,
                                                      spider.algorithm.shingle_based.cluster_size,
                                                      spider.initialize.site_name)
            clustering.process(self.doc_list, distance_matrix)
        else:
            print('There is no clustering algorithm!!')
            return
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