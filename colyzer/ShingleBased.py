__author__ = 'cagdas'

from colyzer import tag_weight
import copy


class Document:
    def __init__(self, doc_name, doc_link=None):
        self.all_paths = []
        self.doc_name = doc_name
        self.doc_link = None

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

    def find_all_hor_paths(self, l, depth):
        temp_list = []
        temp_list_tag = []
        for t in l:
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
                self.find_all_hor_paths(i, depth)


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
        for index_j in range(0,len(self.dists[0])):
            new_value = 0.0
            for index_i in range(0, len(self.dists)):
                new_value += self.dists[index_i][index_j]
            temp_centroid.append(new_value / len(self.dists))
        new_list = copy.copy(temp_centroid)
        self.centroid = new_list