__author__ = 'cagdas'

from colyzer import tag_weight

a = 10
w2 = 1


class Document:
    def __init__(self, real, virtual):
        self.real = real
        self.virtual = virtual


class RealShingles:
    def __init__(self, real_paths, depth):
        self.real_paths = real_paths
        self.depth = depth
        w2 = 1.0
        a = 10.0
        w = 0.0
        for i in range(0, len(self.real_paths)):
            try:
                w1 = tag_weight[self.real_paths[i]]
            except Exception:
                w1 = 0.1
            w3 = (a / ((i + self.depth) + a))
            w += ((w1 * w2 * w3) / len(self.real_paths))
        self.weight = w


class VirtualShingles:
    def __init__(self, virtual_paths, depth):
        self.virtual_paths = virtual_paths
        self.depth = depth
        w2 = 1.0
        a = 10.0
        w = 0.0
        for i in range(0, len(self.virtual_paths)):
            try:
                w1 = tag_weight[self.virtual_paths[i]]
            except Exception:
                w1 = 0.1
            w3 = (a / (self.depth + a))
            w += ((w1 * w2 * w3) / len(self.virtual_paths))
        self.weight = w