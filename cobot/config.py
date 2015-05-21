__author__ = 'cagdas'


class Config:
    def __init__(self, initialize, cobotsettings, algorithm):
        self.initialize = initialize
        self.cobotsettings = cobotsettings
        self.algorithm = algorithm


class Initialize:
    def __init__(self, allowed_domains, start_urls, site_name):
        self.allowed_domains = allowed_domains  # list of allowed domains
        self.start_urls = start_urls  # list of start urls
        self.site_name = site_name  # site folder name


class CobotSettings:
    def __init__(self, robots, page_count):
        self.robots = robots  # obey the robots.txt boolean
        self.page_count = page_count  # page count


class Algorithm:
    def __init__(self, shingle, ted, which):
        self.which = which
        self.shingle = shingle
        self.ted = ted


class ShingleAlgorithm:
    def __init__(self, cluster_size, threshold, iteration):
        self.cluster_size = cluster_size
        self.threshold = threshold
        self.iteration = iteration


class TEDAlgorithm:
    def __init__(self, cluster_size, threshold, iteration):
        self.cluster_size = cluster_size
        self.threshold = threshold
        self.iteration = iteration