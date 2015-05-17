__author__ = 'cagdascaglak'

import os
import copy

from lxml import etree
from colyzer import SITES
import ShingleBased
import TreeEditDistance

if __name__ == '__main__':
    tree = etree.parse('/home/cagdas/Desktop/tree.html', parser=etree.HTMLParser(remove_comments=True))
    root_tag = tree.getroot()[0]

    node = TreeEditDistance.Nodes(root_tag[0])
    print(node.ordered_tree)
    print(node.first_level_subtree)
    for it in node.node_list:
        print(it.ordered_tree)
        for it2 in it.node_list:
            print(it2.ordered_tree)
        print('------------------')
    """
    doc_list = []
    html_files_path = []
    for top_dir0, sub_dirs0, files0 in os.walk(os.path.join(SITES)):
        for site_dir in sub_dirs0:
            for top_dir1, sub_dirs1, page_files in os.walk(os.path.join(top_dir0, site_dir)):
                for html_file in page_files:
                    print(os.path.join(top_dir1, html_file))
                    tree = etree.parse(os.path.join(top_dir1, html_file),
                                       parser=etree.HTMLParser(remove_comments=True))

                    # try:
                    root_tag = tree.getroot()[1]
                    doc = ShingleBased.Document(html_file)
                    doc.find_all_real_paths(root_tag, -1)
                    doc.find_all_virtual_paths(root_tag, 0)
                    doc_list.append(doc)

                    html_files_path.append(os.path.join(top_dir1, html_file))
                    # except Exception:
                    # print(html_file + ' Exp')

    distance_matrix = ShingleBased.get_distance_matrix(doc_list)

    threshold = 0.755
    cluster_size = 5
    clusters = []
    centroids = []

    for i in range(0, cluster_size):
        new_list = copy.copy(distance_matrix[i])
        cluster_obj = ShingleBased.Clusters(new_list)
        cluster_obj.dists.append(new_list)
        new_doc = copy.copy(doc_list[i])
        cluster_obj.docs.append(new_doc)
        cluster_obj.doc_index.append(i)
        clusters.append(cluster_obj)

    for it in range(0, 500):
        print('Iteration --> ' + str(it))

        for d in range(0, len(distance_matrix)):
            temp_max = 0.0
            temp_index = 0
            for c in range(0, len(clusters)):
                similarity = ShingleBased.sim(distance_matrix[d], clusters[c].centroid)
                if similarity > temp_max:
                    print('Max sim = %f' % similarity)
                    temp_max = similarity
                    temp_index = c
            if temp_max > threshold:
                if d in clusters[temp_index].doc_index:
                    if len(clusters[temp_index].doc_index) > 1:
                        index = clusters[temp_index].doc_index.index(d)
                        del clusters[temp_index].doc_index[index]
                        del clusters[temp_index].docs[index]
                        del clusters[temp_index].dists[index]
                        clusters[temp_index].calculate_centroid()
                        new_dists = copy.copy(distance_matrix[d])
                        clusters[temp_index].dists.append(new_dists)
                        new_doc = copy.copy(doc_list[d])
                        clusters[temp_index].docs.append(new_doc)
                        clusters[temp_index].doc_index.append(d)
                else:
                    for cluster_obj in clusters:
                        if d in cluster_obj.doc_index:
                            index = cluster_obj.doc_index.index(d)
                            del cluster_obj.doc_index[index]
                            del cluster_obj.docs[index]
                            del cluster_obj.dists[index]
                    new_dists = copy.copy(distance_matrix[d])
                    clusters[temp_index].dists.append(new_dists)
                    new_doc = copy.copy(doc_list[d])
                    clusters[temp_index].docs.append(new_doc)
                    clusters[temp_index].doc_index.append(d)
                    clusters[temp_index].calculate_centroid()

    for cl in range(0, len(clusters)):
        print('Cluster - %d' % cl)
        for i in range(0, len(clusters[cl].doc_index)):
            print('Doc num: %d, name: %s' % (clusters[cl].doc_index[i], clusters[cl].docs[i].doc_name))
        print('----------------------------------------------')
    """