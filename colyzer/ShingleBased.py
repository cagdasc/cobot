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

import copy
import math

from colyzer import tag_weight


# Calculate similarity between two vectors
def sim(row_i, row_j):
    row_ij_sum = 0
    row_i_sq_sum = 0
    row_j_sq_sum = 0

    for index in range(0, len(row_i)):
        row_ij_sum += row_i[index] * row_j[index]
        row_i_sq_sum += math.pow(row_i[index], 2)
        row_j_sq_sum += math.pow(row_j[index], 2)

    return round(row_ij_sum / (math.sqrt(row_i_sq_sum) * math.sqrt(row_j_sq_sum)), 5)


# Calculate distance with two Document objects
def calculate_distance(doc_0, doc_1):
    intersection_sum0 = 0.0
    diff_sum0 = 0.0
    control = 0

    for index_j in doc_1.all_paths:
        for index_i in doc_0.all_paths:
            if index_j.path == index_i.path:
                control = 1
                intersection_sum0 += abs(index_j.weight - index_i.weight)
        if control == 0:
            diff_sum0 += index_j.weight
        control = 0
    return round(diff_sum0 + intersection_sum0, 5)


# Create distance matrix
def get_distance_matrix(doc_list):
    distance_matrix = []
    i = 0
    j = 0

    temp_max = 0
    for doc_i in doc_list:
        temp_dist = []
        for doc_j in doc_list:
            dist = calculate_distance(doc_i, doc_j)
            temp_dist.append(dist)
            if dist > temp_max:
                temp_max = dist
            print str(i) + ' -- ' + str(j)
            j += 1
        distance_matrix.append(temp_dist)
        j = 0
        i += 1

    for a in range(0, len(distance_matrix)):
        distance_matrix[a] = [round(i / temp_max, 5) for i in distance_matrix[a]]

    return distance_matrix


class Document:
    def __init__(self, doc_name, doc_link=None):
        self.all_paths = []
        self.doc_name = doc_name
        self.doc_link = doc_link

    def find_real_paths(self, tag, tmp_list, d):
        tmp_list.append(tag.tag)
        if len(tag) != 0:
            for t in tag:
                self.find_real_paths(t, tmp_list, d)
        new_list = copy.copy(tmp_list)
        shingles0 = Shingles(new_list, d, 0)
        control = True
        i = 0

        while control and i < len(self.all_paths):
            if shingles0.path == self.all_paths[i].path:
                self.all_paths[i].weight += shingles0.weight
                control = False
            i += 1
        if control:
            self.all_paths.append(shingles0)

        if len(tmp_list) > 0:
            del tmp_list[len(tmp_list) - 1]
        return

    def find_all_real_paths(self, tag, depth):
        depth += 1
        for t in tag:
            temp_list = []
            self.find_real_paths(t, temp_list, depth)
            self.find_all_real_paths(t, depth)

    def find_all_virtual_paths(self, parent, depth):
        temp_list = []
        temp_list_tag = []
        for t in parent:
            temp_list.append(t.tag)
            temp_list_tag.append(t)
        if len(temp_list) is not 0:
            new_list = copy.copy(temp_list)
            shingles0 = Shingles(new_list, depth, 1)
            control = True
            i = 0
            while control and i < len(self.all_paths):
                if shingles0.path == self.all_paths[i].path:
                    self.all_paths[i].weight += shingles0.weight
                    control = False
                i += 1
            if control:
                self.all_paths.append(shingles0)

            depth += 1
            for i in temp_list_tag:
                self.find_all_virtual_paths(i, depth)


class Shingles:
    def __init__(self, path, depth, path_type):
        self.path = path
        self.depth = depth
        w2 = 1.0
        a = 10.0
        w = 0.0
        for i in range(0, len(self.path)):
            try:
                w1 = tag_weight[self.path[i]]
            except Exception, ex:
                w1 = 0.1
            if path_type == 0:
                w3 = (a / ((i + self.depth) + a))
            else:
                w3 = (a / (self.depth + a))
            w += ((w1 * w2 * w3) / len(self.path))
        self.weight = w


class Clusters:
    def __init__(self, centroid):
        self.dists = []
        self.docs = []
        self.doc_index = []
        self.centroid = centroid

    def calculate_centroid(self):
        temp_centroid = []
        for index_j in range(0, len(self.dists[0])):
            new_value = 0.0
            for index_i in range(0, len(self.dists)):
                new_value += self.dists[index_i][index_j]
            temp_centroid.append(new_value / len(self.dists))
        new_list = copy.copy(temp_centroid)
        self.centroid = new_list