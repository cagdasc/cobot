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


class Nodes:
    def __init__(self, root, doc_name, doc_link=None):
        self.root = root
        self.ordered_tree = []
        self.doc_name = doc_name
        self.doc_link = doc_link
        for i in range(0, len(root)):
            self.ordered_tree.append(root[i])
        self.node_list = []
        for child in self.ordered_tree:
            new_node = Nodes(child, doc_name, doc_link)
            self.node_list.append(new_node)


def get_degrees(tag):
    return len(tag)


def cost_insert(node_b):
    return float(len(node_b.root)) + 1.0


def cost_delete(node_a):
    return float(len(node_a.root)) + 1.0


def cost_relabel(node_a, node_b):
    if node_a.root.tag == node_b.root.tag:
        return 0.0
    else:
        return 1.0


def selkow_distance(node_a, node_b):
    m = get_degrees(node_a.root)
    n = get_degrees(node_b.root)

    dist = [[0.0 for j in range(n + 1)] for i in range(m + 1)]
    dist[0][0] = cost_relabel(node_a, node_b)
    # print(node_a.root.tag + ' - ' + node_b.root.tag + '-->' + str(dist[0][0]))

    for j in range(1, n + 1):
        dist[0][j] = dist[0][j - 1] + cost_insert(node_b.node_list[j - 1])

    for i in range(1, m + 1):
        dist[i][0] = dist[i - 1][0] + cost_delete(node_a.node_list[i - 1])

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            dist[i][j] = min(
                dist[i - 1][j - 1] + selkow_distance(node_a.node_list[i - 1], node_b.node_list[j - 1]),
                dist[i][j - 1] + cost_insert(node_b.node_list[j - 1]),
                dist[i - 1][j] + cost_delete(node_a.node_list[i - 1]))
    # print(dist)
    # print('------------------' + str(dist[m][n]))
    return dist[m][n]


def get_distance_matrix(doc_list):
    ted_dist = []
    for i in range(0, len(doc_list)):
        temp_list = []
        for j in range(0, len(doc_list)):
            dist = selkow_distance(doc_list[i], doc_list[j])
            print('dist %d - %d = %d' % (i, j, dist))
            temp_list.append(dist)
        ted_dist.append(temp_list)

    distance_matrix = []
    temp_max = 0.0
    for i in range(0, len(ted_dist)):
        for j in range(i + 1, len(ted_dist[i])):
            if ted_dist[i][j] > temp_max:
                temp_max = ted_dist[i][j]

    for a in range(0, len(ted_dist)):
        temp = [round(i / temp_max, 5) for i in ted_dist[a]]
        distance_matrix.append(temp)

    return distance_matrix
