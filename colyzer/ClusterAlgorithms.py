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
import sys
import copy
import math
import json
from cobot.spiders import SITES


class Clusters:
    def __init__(self, centroid):
        self.dists = []
        self.docs = []
        self.doc_index = []
        self.centroid = centroid

    def calculate_centroid(self):
        if len(self.dists) > 0:
            temp_centroid = []
            for index_j in range(0, len(self.dists[0])):
                new_value = 0.0
                for index_i in range(0, len(self.dists)):
                    new_value += self.dists[index_i][index_j]
                temp_centroid.append(new_value / len(self.dists))
            new_list = copy.copy(temp_centroid)
            self.centroid = new_list


class Clustering:
    def __init__(self, threshold, iteration, cluster_size, site_name):
        self.threshold = threshold
        self.iteration = iteration
        self.cluster_size = cluster_size
        self.clusters = []
        self.site_name = site_name

    # Calculate similarity between two vectors
    def sim(self, row_i, row_j):
        row_ij_sum = 0
        row_i_sq_sum = 0
        row_j_sq_sum = 0

        for index in range(0, len(row_i)):
            row_ij_sum += row_i[index] * row_j[index]
            row_i_sq_sum += math.pow(row_i[index], 2)
            row_j_sq_sum += math.pow(row_j[index], 2)

        return round(row_ij_sum / (math.sqrt(row_i_sq_sum) * math.sqrt(row_j_sq_sum)), 5)

    def k_means_process(self, doc_list, distance_matrix):
        print('Distance Matrix length: %d' % len(distance_matrix))
        print('Cluster Size: %d' % self.cluster_size)

        for i in range(0, self.cluster_size):  # clusters initialization
            new_list = copy.copy(distance_matrix[i])
            cluster_obj = Clusters(new_list)
            cluster_obj.dists.append(new_list)
            new_doc = copy.copy(doc_list[i])
            cluster_obj.docs.append(new_doc)
            cluster_obj.doc_index.append(i)
            self.clusters.append(cluster_obj)

        for cl in self.clusters:
            print(cl.doc_index)

        for it in range(0, self.iteration):
            print('Iteration --> ' + str(it))
            for d in range(0, len(distance_matrix)):
                temp_min = float(sys.maxint)
                temp_index = 0
                for c in range(0, len(self.clusters)):
                    dist = self.euclidean_distance(distance_matrix[d], self.clusters[c].centroid)
                    if dist < temp_min:
                        temp_min = dist
                        temp_index = c
                if d not in self.clusters[temp_index].doc_index:
                    """
                    for cluster_obj in self.clusters:  # delete this vector, add new cluster and calculate new centroid
                        if d in cluster_obj.doc_index:
                            index = cluster_obj.doc_index.index(d)
                            del cluster_obj.doc_index[index]
                            del cluster_obj.docs[index]
                            del cluster_obj.dists[index]
                    """
                    i = 0
                    is_in = False
                    while i < len(self.clusters) and not is_in:
                        if d in self.clusters[i].doc_index:
                            index = self.clusters[i].doc_index.index(d)
                            del self.clusters[i].doc_index[index]
                            del self.clusters[i].docs[index]
                            del self.clusters[i].dists[index]
                            is_in = True
                        i += 1

                    new_dists = copy.copy(distance_matrix[d])
                    self.clusters[temp_index].dists.append(new_dists)
                    new_doc = copy.copy(doc_list[d])
                    self.clusters[temp_index].docs.append(new_doc)
                    self.clusters[temp_index].doc_index.append(d)
            for c in self.clusters:
                c.calculate_centroid()

        cluster_list = []
        for cluster in self.clusters:
            result_doc_list = []
            for doc in cluster.docs:
                result_doc = Document(doc.doc_name, doc.doc_link)
                result_doc_list.append(result_doc.__dict__)
            cluster_list.append(result_doc_list)
        result = Result(cluster_list)

        json_txt = json.dumps(result.__dict__)
        with open(os.path.join(SITES, self.site_name + '.json'), 'w') as f:
            f.write(json_txt)

    def euclidean_distance(self, vector_0, vector_1):
        sum_v = 0.0
        for i in range(0, len(vector_0)):
            sum_v += math.pow(vector_0[i] - vector_1[i], 2)
        return math.sqrt(sum_v)

    def shingle_based_process(self, doc_list, distance_matrix):
        for i in range(0, self.cluster_size):  # clusters initialization
            new_list = copy.copy(distance_matrix[i])
            cluster_obj = Clusters(new_list)
            cluster_obj.dists.append(new_list)
            new_doc = copy.copy(doc_list[i])
            cluster_obj.docs.append(new_doc)
            cluster_obj.doc_index.append(i)
            self.clusters.append(cluster_obj)

        for it in range(0, self.iteration):
            print('Iteration --> ' + str(it))

            for d in range(0, len(distance_matrix)):
                temp_max = 0.0
                temp_index = 0
                for c in range(0, len(self.clusters)):
                    similarity = self.sim(distance_matrix[d], self.clusters[c].centroid)  # compare vector with
                    if similarity > temp_max:  # find max similarity                    # all clusters centroid
                        print('Max sim = %f' % similarity)
                        temp_max = similarity
                        temp_index = c
                if temp_max > self.threshold:  # if max sim greater than threshold
                    if d in self.clusters[temp_index].doc_index:  # if chosen vector has in compared cluster after delete
                        if len(self.clusters[temp_index].doc_index) > 1:  # this vector, calculate new centroid and add the vector
                            index = self.clusters[temp_index].doc_index.index(d)
                            del self.clusters[temp_index].doc_index[index]
                            del self.clusters[temp_index].docs[index]
                            del self.clusters[temp_index].dists[index]
                            self.clusters[temp_index].calculate_centroid()
                            new_dists = copy.copy(distance_matrix[d])
                            self.clusters[temp_index].dists.append(new_dists)
                            new_doc = copy.copy(doc_list[d])
                            self.clusters[temp_index].docs.append(new_doc)
                            self.clusters[temp_index].doc_index.append(d)
                    else:  # if chosen vector not in this compared cluster, look other cluster and if it is already
                        """
                        for cluster_obj in self.clusters:  # delete this vector, add new cluster and calculate new centroid
                            if d in cluster_obj.doc_index:
                                index = cluster_obj.doc_index.index(d)
                                del cluster_obj.doc_index[index]
                                del cluster_obj.docs[index]
                                del cluster_obj.dists[index]
                        """
                        i = 0
                        is_in = False
                        while i < len(self.clusters) and not is_in:
                            if d in self.clusters[i].doc_index:
                                index = self.clusters[i].doc_index.index(d)
                                del self.clusters[i].doc_index[index]
                                del self.clusters[i].docs[index]
                                del self.clusters[i].dists[index]
                                is_in = True
                            i += 1
                        new_dists = copy.copy(distance_matrix[d])
                        self.clusters[temp_index].dists.append(new_dists)
                        new_doc = copy.copy(doc_list[d])
                        self.clusters[temp_index].docs.append(new_doc)
                        self.clusters[temp_index].doc_index.append(d)
                        self.clusters[temp_index].calculate_centroid()

        cluster_list = []
        for cluster in self.clusters:
            result_doc_list = []
            for doc in cluster.docs:
                result_doc = Document(doc.doc_name, doc.doc_link)
                result_doc_list.append(result_doc.__dict__)
            cluster_list.append(result_doc_list)
        result = Result(cluster_list)

        json_txt = json.dumps(result.__dict__)
        with open(os.path.join(SITES, self.site_name + '.json'), 'w') as f:
            f.write(json_txt)

    def pretty_print(self):
        for cl in range(0, len(self.clusters)):
            print('Cluster - %d' % cl)
            for i in range(0, len(self.clusters[cl].doc_index)):
                print('Doc num: %d, name: %s, link: %s' % (self.clusters[cl].doc_index[i],
                                                           self.clusters[cl].docs[i].doc_name,
                                                           self.clusters[cl].docs[i].doc_link))
            print('----------------------------------------------')


class Result:
    def __init__(self, cluster_list):
        self.cluster_list = cluster_list


class Document:
    def __init__(self, doc_name, doc_link):
        self.doc_name = doc_name
        self.doc_link = doc_link