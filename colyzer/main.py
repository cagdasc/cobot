__author__ = 'cagdascaglak'

import os
import copy

from lxml import etree

from colyzer import SITES
from colyzer.Document import RealShingles, VirtualShingles, Document


real_paths = []
virtual_hor = []


def find_real_paths(tag, tmp_list, d):
    tmp_list.append(tag.tag)
    if len(tag) != 0:
        for t in tag:
            find_real_paths(t, tmp_list, d)
    new_list = copy.copy(tmp_list)
    if len(new_list) > 2:
        for i in range(0, len(new_list) - 2):
            new_shingle_list = [new_list[i], new_list[i + 1], new_list[i + 2]]
            real_shingles = RealShingles(new_shingle_list, d)
            real_paths.append(real_shingles)
    if len(tmp_list) > 0:
        del tmp_list[len(tmp_list) - 1]
    return


def find_all_real_paths(tag, depth):
    depth += 1
    for t in tag:
        temp_list = []
        find_real_paths(t, temp_list, depth)
        find_all_real_paths(t, depth)


def find_all_hor_paths(l, depth):
    temp_list = []
    temp_list_tag = []
    for t in l:
        temp_list.append(t.tag)
        temp_list_tag.append(t)
    if len(temp_list) is not 0:
        new_list = copy.copy(temp_list)
        virtual_shingles = VirtualShingles(new_list, depth)
        virtual_hor.append(virtual_shingles)
        depth += 1
        for i in temp_list_tag:
            find_all_hor_paths(i, depth)


def calculate_distance(doci, docj):
    intersection_sum0 = 0.0
    diff_sum0 = 0.0
    control = 0

    for j in docj.real:
        for i in doci.real:
            if j.real_paths == i.real_paths:
                control = 1
                intersection_sum0 += abs(j.weight - i.weight)
        if control == 0:
            diff_sum0 += j.weight
        control = 0


    control = 0
    intersection_sum1 = 0.0
    diff_sum1 = 0.0
    for j in docj.virtual:
        for i in doci.virtual:
            if j.virtual_paths == i.virtual_paths:
                control = 1
                intersection_sum1 += abs(j.weight - i.weight)
        if control == 0:
            diff_sum1 += j.weight
        control = 0
    return diff_sum0 + intersection_sum0 + diff_sum1 + intersection_sum1


if __name__ == '__main__':
    doc_list = []
    html_files_path = []
    for top_dir0, sub_dirs0, files0 in os.walk(os.path.join(SITES)):
        for site_dir in sub_dirs0:
            for top_dir1, sub_dirs1, page_files in os.walk(os.path.join(top_dir0, site_dir)):
                for html_file in page_files:

                    print(os.path.join(top_dir1, html_file))
                    tree = etree.parse(os.path.join(top_dir1, html_file),
                                       parser=etree.HTMLParser(remove_comments=True))

                    try:
                        root_tag = tree.getroot()[1]
                        find_all_real_paths(root_tag, -1)
                        find_all_hor_paths(root_tag, 0)

                        new_real = copy.copy(real_paths)
                        new_virtual = copy.copy(virtual_hor)

                        doc = Document(new_real, new_virtual)
                        doc_list.append(doc)

                        del real_paths[:]
                        del virtual_hor[:]

                        html_files_path.append(os.path.join(top_dir1, html_file))
                    except Exception:
                        print(html_file)

    distance_matrix = []

    for doci in doc_list:
        temp_dist = []
        for docj in doc_list:
            dist = calculate_distance(doci, docj)
            temp_dist.append(dist)
        distance_matrix.append(temp_dist)

    for a in distance_matrix:
        print(a)


