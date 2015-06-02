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
import sys
import time

from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from scrapy.utils.project import get_project_settings
from lxml import etree

import ShingleBased
import SelkowTED
import ClusterAlgorithms
from cobot.spiders import SITES
from cobot.spiders.crawler import PageWalker
from cobot.pipelines import get_all_form, create_tree

if __name__ == '__main__':

    # print(os.environ['PYTHONPATH'])

    with open(sys.argv[1]) as f:
        config_file = f.read()
        print(config_file)
        __config = json.loads(config_file, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

    cluster_size = 0
    if __config.algorithm.which_clustering == 'kmeans':
        cluster_size = __config.algorithm.k_means.cluster_size
    elif __config.algorithm.which_clustering == 'sbc':
        cluster_size = __config.algorithm.shingle_based.cluster_size

    if __config.cobot_settings.page_count < cluster_size:
        print('Number of clusters must be less than number of pages!!')
        sys.exit(status=1)

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
        start = time.time()  # start time
        algorithm = __config.algorithm.which
        doc_list = []

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

                if algorithm == 'sbsa':
                    form_list = []
                    get_all_form(root_tag, form_list)
                    temp_root = etree.Element('root')
                    create_tree(temp_root, form_list)

                    doc = ShingleBased.ShingleDocument(html_file, doc_link=doc_link)
                    doc.find_all_real_paths(temp_root, -1)
                    doc.find_all_virtual_paths(temp_root, 0)
                    doc_list.append(doc)
                elif algorithm == 'ted':
                    form_list = []
                    get_all_form(root_tag, form_list)
                    temp_root = etree.Element('root')
                    create_tree(temp_root, form_list)

                    doc = SelkowTED.Nodes(temp_root, doc_name=html_file, doc_link=doc_link)
                    doc_list.append(doc)

                else:
                    print('There is no algorithm!!')
        distance_matrix = []
        if algorithm == 'sbsa':
            distance_matrix = ShingleBased.get_distance_matrix(doc_list)
            print(distance_matrix)
        elif algorithm == 'ted':
            distance_matrix = SelkowTED.get_distance_matrix(doc_list)
            print(distance_matrix)
        else:
            print('There is no algorithm!!')

        middle = time.time()  # analyze algorithm time diff

        if __config.algorithm.which_clustering == 'kmeans':
            clustering = ClusterAlgorithms.Clustering(__config.algorithm.k_means.iteration,
                                                      __config.algorithm.k_means.cluster_size,
                                                      __config.initialize.site_name,
                                                      algorithm)
            clustering.k_means_process(doc_list, distance_matrix)
            clustering.pretty_print()
        elif __config.algorithm.which_clustering == 'sbc':
            clustering = ClusterAlgorithms.Clustering(__config.algorithm.shingle_based.iteration,
                                                      __config.algorithm.shingle_based.cluster_size,
                                                      __config.initialize.site_name,
                                                      algorithm)
            clustering.shingle_based_process(doc_list, distance_matrix)
            clustering.pretty_print()
        else:
            print('There is no clustering algorithm!!')

        end = time.time()  # end time

        print('Analyze algorithm time diff %f' % (middle - start))
        print('Clustering algorithm time diff: %f' % (end - middle))
        print('Total time diff: %f' % (end - start))
