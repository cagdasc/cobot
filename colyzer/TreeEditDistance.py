__author__ = 'cagdas'


class Nodes:
    def __init__(self, root):
        self.root = root
        self.ordered_tree = []
        self.first_level_subtree = []
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


def cost_relabel(tag_a, tag_b):
    if tag_a.tag == tag_b.tag:
        return 0
    else:
        return 1


def cost_graft():
    pass


def cost_prune():
    pass


def contained(node_p, node, con):
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
            print('***')
            con.append(True)
            return True
        else:
            return False
    else:
        return False


def containedIn(node_p, node, con):
    value = contained(node_p, node, con)

    if not value:
        for new_node in node.node_list:
            containedIn(node_p, new_node, con)
        return False
    else:
        return value


def edit_distance(node_a, node_b):
    m = get_degrees(node_a.root)
    n = get_degrees(node_b.root)

    if m == 0 or n == 0:
        return 0

    dist = [[0 for j in range(n + 1)] for i in range(m + 1)]
    dist[0][0] = cost_relabel(node_a.root, node_b.root)

    for j in range(1, n + 1):
        dist[0][j] = dist[0][j - 1] + cost_graft()

    for i in range(1, m + 1):
        dist[i][0] = dist[i - 1][0] + cost_prune()