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
        with open(os.path.join(SITES, spider.main_site + '_raw.json'), 'w') as f:
            f.write(json_txt)

        if spider.algorithm.which == 'sbsa':
            distance_matrix = ShingleBased.get_distance_matrix(self.doc_list)
            print(distance_matrix)
        elif spider.algorithm.which == 'ted':
            distance_matrix = SelkowTED.get_distance_matrix(self.doc_list)
            print(distance_matrix)
        else:
            print('There is no algorithm!!')
            return

        if spider.algorithm.which_clustering == 'kmeans':
            clustering = ClusterAlgorithms.Clustering(spider.algorithm.k_means.iteration,
                                                      spider.algorithm.k_means.cluster_size,
                                                      spider.main_site,
                                                      spider.algorithm.which)
            clustering.k_means_process(self.doc_list, distance_matrix)
        elif spider.algorithm.which_clustering == 'sbc':
            clustering = ClusterAlgorithms.Clustering(spider.algorithm.shingle_based.iteration,
                                                      spider.algorithm.shingle_based.cluster_size,
                                                      spider.main_site,
                                                      spider.algorithm.which)
            clustering.shingle_based_process(self.doc_list, distance_matrix)
        else:
            print('There is no clustering algorithm!!')
            return
        clustering.pretty_print()

    def __create_doc_list(self, item, which):
        tree = etree.parse(item['page_full_path'], parser=etree.HTMLParser(remove_comments=True))
        root_tag = tree.getroot()[1]
        if which == 'sbsa':
            form_list = []
            get_all_form(root_tag, form_list)
            temp_root = etree.Element('root')
            create_tree(temp_root, form_list)

            doc = ShingleBased.ShingleDocument(doc_name=item['page_name'], doc_link=item['page_url'])
            doc.find_all_real_paths(temp_root, -1)
            doc.find_all_virtual_paths(temp_root, 0)
            self.doc_list.append(doc)
        elif which == 'ted':
            form_list = []
            get_all_form(root_tag, form_list)
            temp_root = etree.Element('root')
            create_tree(temp_root, form_list)

            doc = SelkowTED.Nodes(temp_root, doc_name=item['page_name'], doc_link=item['page_url'])
            self.doc_list.append(doc)


def get_all_form(tag, form_list):
    for t in tag:
        if t.tag == 'form':
            form_list.append(t)
        else:
            get_all_form(t, form_list)


def create_tree(root, children):
    for child in children:
        new_child = etree.SubElement(root, child.tag)
        create_tree(new_child, child)