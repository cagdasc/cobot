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