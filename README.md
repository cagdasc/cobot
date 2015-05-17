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