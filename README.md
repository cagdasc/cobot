# cobot
The aim of this project is analysing web pages and classifying them with machine
learning methods to find out the common security vulnerabilities in similar web pages. 
The reason we have chosen this project is that the most of the works been made in this 
area are for XML documents and our purpose is applying the existing approaches and 
methods for HTML documents.

The project involves developing a web crawler based on the features we defined. This 
web crawler scans a given domain and pulls all the pages that contain form tags since 
input fields can have security vulnerabilities. As the next step, these pages are classified 
based on their structural similarities with machine learning methods. Then, a page from 
each cluster is chosen and security tests are applied to these pages. If there are 
vulnerabilities in a chosen page, it can be said that all the pages in its cluster, have the 
same vulnerabilities. Thanks to this approach, the cost and time of full site security 
analysis is reduced.

##Usage
	{ "crawling": true|false, 
	  "initialize": {
	    "allowed_domains": ["allowed domains for crawling web site"],
	    "start_urls": ["start urls"], 
	    "site_name": "crawled sites folder name"
	  },
	  "cobot_settings": {
	    "robots": true|false for obey robots.txt,
	    "page_count": 100
	  },
	  "algorithm": {
	    "which": "sbsa|ted structural analyzing algorithim",
	    "which_clustering": "sbc|kmeans clustering algorithm",
	    "k_means": {
	      "cluster_size": int cluster size,
	      "iteration": int iteration count
	    },
	    "shingle_based": {
	      "cluster_size": int cluster size,
	      "iteration": int iteration count
	    }
	  }
	}
	export PYTHONPATH=/project/root
	python colyzer/main.py sites/config/site.cfg

##License
	Copyright 2015 Cagdas Caglak

	Licensed under the Apache License, Version 2.0 (the "License");
	you may not use this file except in compliance with the License.
	You may obtain a copy of the License at

	http://www.apache.org/licenses/LICENSE-2.0

	Unless required by applicable law or agreed to in writing, software
	distributed under the License is distributed on an "AS IS" BASIS,
	WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
	See the License for the specific language governing permissions and
	limitations under the License.