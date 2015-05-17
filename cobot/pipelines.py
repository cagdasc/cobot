# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from lxml import etree
from colyzer import ShingleBased


class CobotPipeline(object):
    def __init__(self):
        self.doc_list = []

    def open_spider(self, spider):
        print('OPENED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!111111')

    def process_item(self, item, spider):
        print('page name -->' + item['page_name'])
        print('Processing....')
        self.__create_doc_list(item)
        print('doc list len -->>>> %d' % len(self.doc_list))
        print(spider.name)

        return item

    def close_spider(self, spider):
        distance_matrix = ShingleBased.get_distance_matrix(self.doc_list)

    def __create_doc_list(self, item):
        tree = etree.parse(item['page_full_path'], parser=etree.HTMLParser(remove_comments=True))
        root_tag = tree.getroot()[1]
        doc = ShingleBased.Document(doc_name=item['page_name'], doc_link=item['page_url'])
        doc.find_all_real_paths(root_tag, -1)
        doc.find_all_virtual_paths(root_tag, 0)
        self.doc_list.append(doc)