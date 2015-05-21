# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from lxml import etree
from colyzer import ShingleBased, SelkowTED
import copy


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
        if spider.algorithm.which == 'shingle':
            distance_matrix = ShingleBased.get_distance_matrix(self.doc_list)
            threshold = spider.algorithm.shingle.threshold
            cluster_size = spider.algorithm.shingle.cluster_size
            clusters = []

            for i in range(0, cluster_size):  # clusters initialization
                new_list = copy.copy(distance_matrix[i])
                cluster_obj = ShingleBased.Clusters(new_list)
                cluster_obj.dists.append(new_list)
                new_doc = copy.copy(self.doc_list[i])
                cluster_obj.docs.append(new_doc)
                cluster_obj.doc_index.append(i)
                clusters.append(cluster_obj)
            for it in range(0, spider.algorithm.shingle.iteration):
                print('Iteration --> ' + str(it))
                for d in range(0, len(distance_matrix)):
                    temp_max = 0.0
                    temp_index = 0
                    for c in range(0, len(clusters)):
                        similarity = ShingleBased.sim(distance_matrix[d],
                                                      clusters[c].centroid)  # compare vector with all clusters centroid
                        if similarity > temp_max:  # find max similarity
                            print('Max sim = %f' % similarity)
                            temp_max = similarity
                            temp_index = c
                    if temp_max > threshold:  # if max sim greater than threshold
                        if d in clusters[temp_index].doc_index:  # if chosen vector has in compared cluster after delete
                            if len(clusters[temp_index].doc_index) > 1:  # this vector, calculate new centroid and add the vector
                                index = clusters[temp_index].doc_index.index(d)
                                del clusters[temp_index].doc_index[index]
                                del clusters[temp_index].docs[index]
                                del clusters[temp_index].dists[index]
                                clusters[temp_index].calculate_centroid()
                                new_dists = copy.copy(distance_matrix[d])
                                clusters[temp_index].dists.append(new_dists)
                                new_doc = copy.copy(self.doc_list[d])
                                clusters[temp_index].docs.append(new_doc)
                                clusters[temp_index].doc_index.append(d)
                        else:  # if chosen vector not in this compared cluster, look other cluster and if it is already
                            for cluster_obj in clusters:  # delete this vector, add new cluster and calculate new centroid
                                if d in cluster_obj.doc_index:
                                    index = cluster_obj.doc_index.index(d)
                                    del cluster_obj.doc_index[index]
                                    del cluster_obj.docs[index]
                                    del cluster_obj.dists[index]
                            new_dists = copy.copy(distance_matrix[d])
                            clusters[temp_index].dists.append(new_dists)
                            new_doc = copy.copy(self.doc_list[d])
                            clusters[temp_index].docs.append(new_doc)
                            clusters[temp_index].doc_index.append(d)
                            clusters[temp_index].calculate_centroid()
        elif spider.algorithm.which == 'ted':
            for i in range(0, len(self.doc_list)):
                temp_list = []
                for j in range(0, len(self.doc_list)):
                    dist = SelkowTED.selkow_distance(self.doc_list[i], self.doc_list[j])
                    print('dist %d - %d = %d' % (i, j, dist))
                    temp_list.append(dist)
                self.ted_dist.append(temp_list)
            distance_matrix = SelkowTED.normalize_distance_matrix(self.ted_dist)
            print(distance_matrix)

            threshold = spider.algorithm.ted.threshold
            cluster_size = spider.algorithm.ted.cluster_size
            clusters = []

            for i in range(0, cluster_size):  # clusters initialization
                new_list = copy.copy(distance_matrix[i])
                cluster_obj = ShingleBased.Clusters(new_list)
                cluster_obj.dists.append(new_list)
                new_doc = copy.copy(self.doc_list[i])
                cluster_obj.docs.append(new_doc)
                cluster_obj.doc_index.append(i)
                clusters.append(cluster_obj)

            for it in range(0, spider.algorithm.ted.iteration):
                print('Iteration --> ' + str(it))

                for d in range(0, len(distance_matrix)):
                    temp_max = 0.0
                    temp_index = 0
                    for c in range(0, len(clusters)):
                        similarity = ShingleBased.sim(distance_matrix[d],
                                                      clusters[c].centroid)  # compare vector with all clusters centroid
                        if similarity > temp_max:  # find max similarity
                            print('Max sim = %f' % similarity)
                            temp_max = similarity
                            temp_index = c
                    if temp_max > threshold:  # if max sim greater than threshold
                        if d in clusters[temp_index].doc_index:  # if chosen vector has in compared cluster after delete
                            if len(clusters[temp_index].doc_index) > 1:  # this vector, calculate new centroid and add the vector
                                index = clusters[temp_index].doc_index.index(d)
                                del clusters[temp_index].doc_index[index]
                                del clusters[temp_index].docs[index]
                                del clusters[temp_index].dists[index]
                                clusters[temp_index].calculate_centroid()
                                new_dists = copy.copy(distance_matrix[d])
                                clusters[temp_index].dists.append(new_dists)
                                new_doc = copy.copy(self.doc_list[d])
                                clusters[temp_index].docs.append(new_doc)
                                clusters[temp_index].doc_index.append(d)
                        else:  # if chosen vector not in this compared cluster, look other cluster and if it is already
                            for cluster_obj in clusters:  # delete this vector, add new cluster and calculate new centroid
                                if d in cluster_obj.doc_index:
                                    index = cluster_obj.doc_index.index(d)
                                    del cluster_obj.doc_index[index]
                                    del cluster_obj.docs[index]
                                    del cluster_obj.dists[index]
                            new_dists = copy.copy(distance_matrix[d])
                            clusters[temp_index].dists.append(new_dists)
                            new_doc = copy.copy(self.doc_list[d])
                            clusters[temp_index].docs.append(new_doc)
                            clusters[temp_index].doc_index.append(d)
                            clusters[temp_index].calculate_centroid()
            for cl in range(0, len(clusters)):
                print('Cluster - %d' % cl)
                for i in range(0, len(clusters[cl].doc_index)):
                    print('Doc num: %d, name: %s' % (clusters[cl].doc_index[i], clusters[cl].docs[i].doc_name))
                print('----------------------------------------------')

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