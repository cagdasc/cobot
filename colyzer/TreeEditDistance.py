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
    def __init__(self, root):
        self.root = root
        self.ordered_tree = []
        self.first_level_subtree = []
        if len(root) == 0:
            self.is_leaf = True
        else:
            self.is_leaf = False
        for i in range(0, len(root)):
            self.ordered_tree.append(root[i])
            temp_list = []
            for j in root[i]:
                temp_list.append(j)
            self.first_level_subtree.append(temp_list)
        self.node_list = []
        for child in self.ordered_tree:
            new_node = Nodes(child)
            self.node_list.append(new_node)


def get_degrees(tag):
    return len(tag)


def tree_eq(node_a, node_b):
    ctrl = True
    if node_a.root.tag == node_b.root.tag and len(node_a.root) == len(node_b.root):
        i = 0
        while i < len(node_a.root) and ctrl:
            if node_a.ordered_tree[i].tag == node_b.ordered_tree[i].tag \
                    and len(node_a.ordered_tree[i]) == len(node_b.ordered_tree[i]):
                j = 0
                while j < len(node_a.node_list[i].ordered_tree) and ctrl:
                    if node_b.node_list[i].ordered_tree[j].tag != \
                            node_a.node_list[i].ordered_tree[j].tag:
                        ctrl = False
                    j += 1
            else:
                ctrl = False
            i += 1
        return ctrl
    else:
        return False


def tree_eq_cost(node_a, node_b):
    cost = 0
    ctrl = True
    if node_a.root.tag != node_b.root.tag:
        cost += 1
    i = 0
    j = 0
    while i < len(node_a.node_list):
        checker = True
        while j < len(node_b.node_list) and checker:
            if node_a.node_list[i].root.tag == node_b.node_list[j].root.tag:
                # cost += 1
                checker = False
            j += 1
        if not checker:
            k = 0
            l = 0
            while k < len(node_a.node_list[i].ordered_tree):
                while l < len(node_b.node_list[j - 1].ordered_tree):
                    if node_a.node_list[i].ordered_tree[k].tag != node_b.node_list[j].ordered_tree[l].tag:
                        cost += 1
                    l += 1
                k += 1
            # j += 1
        else:
            cost += len(node_a.node_list[i].root)
        i += 1
    return cost


def node_eq(node_a, node_b):
    if node_a.root.tag == node_b.root.tag:
        return True
    else:
        return False


def cost_relabel(node_a, node_b):
    if node_eq(node_a, node_b):
        return 0
    else:
        return 1


def cost_graft(node_b, node_a=None, mode=0):
    if mode == 0:
        return len(node_b.root) + 1
    else:
        d0 = 1
        d0 += len(node_b.root)

        d1 = 0
        if containedIn(node_b, node_a):
            d1 += (len(node_b.root) + 1)
        return min(d0, d1)


def cost_prune(node_a, node_b=None, mode=0):
    if mode == 0:
        return len(node_a.root) + 1
    else:
        d0 = 1
        d0 += len(node_a.root)

        d1 = 0
        if containedIn(node_a, node_b):
            d1 += (len(node_a.root) + 1)
        return min(d0, d1)


def contained(node_p, node):
    if node_p.root.tag == node.root.tag:
        pairs_0 = 0
        j = 0
        for i in range(0, len(node_p.ordered_tree)):
            check0 = True
            while j < len(node.ordered_tree) and check0:
                if node_p.ordered_tree[i].tag == node.ordered_tree[j].tag:
                    l = 0
                    pairs_01 = 0
                    for k in range(0, len(node_p.first_level_subtree[i])):
                        check1 = True
                        while l < len(node.first_level_subtree[j]) and check1:
                            if node_p.first_level_subtree[i][k].tag == node.first_level_subtree[j][l].tag:
                                check1 = False
                                pairs_01 += 1

                            l += 1
                    if pairs_01 == len(node_p.first_level_subtree[i]):
                        pairs_0 += 1
                    check0 = False
                j += 1
        if pairs_0 == len(node_p.ordered_tree):
            if node_p.is_leaf and node.is_leaf:
                print('!!!')
                return True
            elif node_p.is_leaf and not node.is_leaf:
                return False
            else:
                print('***')
                return True
        else:
            return False
    else:
        return False


def containedIn(node_p, node):
    value = contained(node_p, node)
    if not value:
        for new_node in node.node_list:
            result = containedIn(node_p, new_node)
            if result:
                return True
        return False
    else:
        return value


def edit_distance(node_a, node_b, org_node_a, org_node_b):
    m = get_degrees(node_a.root)
    n = get_degrees(node_b.root)

    dist = [[0 for j in range(n + 1)] for i in range(m + 1)]
    dist[0][0] = cost_relabel(node_a, node_b)
    print(node_a.root.tag + ' - ' + node_b.root.tag + '-->' + str(dist[0][0]))

    for j in range(1, n + 1):
        dist[0][j] = dist[0][j - 1] + cost_graft(node_b.node_list[j - 1])

    for i in range(1, m + 1):
        dist[i][0] = dist[i - 1][0] + cost_prune(node_a.node_list[i - 1])

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            dist[i][j] = min(
                dist[i - 1][j - 1] + edit_distance(node_a.node_list[i - 1], node_b.node_list[j - 1], org_node_a,
                                                   org_node_b),
                dist[i][j - 1] + cost_graft(node_b.node_list[j - 1], org_node_a, mode=1),
                dist[i - 1][j] + cost_prune(node_a.node_list[i - 1], org_node_b, mode=1))
    print(dist)
    print('------------------' + str(dist[m][n]))
    return dist[m][n]