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


def edit_distance(node_a, node_b):
    m = get_degrees(node_a.root)
    n = get_degrees(node_b.root)

    if m == 0 or n == 0:
        return 0

    dist = [[0 for j in range(n)] for i in range(m)]

    for j in range(1, n):
        dist[0][j] = dist[0][j - 1] + cost_graft()

    for i in range(1, m):
        dist[i][0] = dist[i - 1][0] + cost_prune()