__author__ = 'cagdas'


class Config:
    def __init__(self, crawling, initialize, cobot_settings, algorithm):
        self.crawling = crawling
        self.initialize = initialize
        self.cobot_settings = cobot_settings
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
    def __init__(self, k_means, shingle_based, which, which_clustering):
        self.which = which
        self.which_clustering = which_clustering
        self.k_means = k_means
        self.shingle_based = shingle_based


class KMeansAlgorithm:
    def __init__(self, cluster_size, iteration):
        self.cluster_size = cluster_size
        self.iteration = iteration


class ShingleBasedAlgorithm:
    def __init__(self, cluster_size, threshold, iteration):
        self.cluster_size = cluster_size
        self.threshold = threshold
        self.iteration = iteration