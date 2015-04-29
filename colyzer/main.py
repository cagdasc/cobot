__author__ = 'cagdascaglak'

import os
import copy

from lxml import etree

from colyzer import SITES
import ShingleBased

all_paths = []


def find_real_paths(tag, tmp_list, d):
    tmp_list.append(tag.tag)
    if len(tag) != 0:
        for t in tag:
            find_real_paths(t, tmp_list, d)
    new_list = copy.copy(tmp_list)
    shingles0 = ShingleBased.Shingles(new_list, d, 0)
    cntrl = True
    i = 0

    while cntrl and i < len(all_paths):
        if shingles0.path == all_paths[i].path:
            all_paths[i].weight += shingles0.weight
            cntrl = False
        i += 1
    if cntrl:
        all_paths.append(shingles0)

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
        shingles0 = ShingleBased.Shingles(new_list, depth, 1)
        cntrl = True
        i = 0
        while cntrl and i < len(all_paths):
            if shingles0.path == all_paths[i].path:
                all_paths[i].weight += shingles0.weight
                cntrl = False
            i += 1
        if cntrl:
            all_paths.append(shingles0)

        depth += 1
        for i in temp_list_tag:
            find_all_hor_paths(i, depth)


def calculate_distance(doci, docj):
    intersection_sum0 = 0.0
    diff_sum0 = 0.0
    control = 0

    for j in docj.all_paths:
        for i in doci.all_paths:
            if j.path == i.path:
                control = 1
                intersection_sum0 += abs(j.weight - i.weight)
        if control == 0:
            diff_sum0 += j.weight
        control = 0
    return diff_sum0 + intersection_sum0


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

                    # try:
                    root_tag = tree.getroot()[1]
                    doc = ShingleBased.Document()
                    doc.find_all_real_paths(root_tag, -1)
                    doc.find_all_hor_paths(root_tag, 0)
                    doc_list.append(doc)


                    """
                    find_all_real_paths(root_tag, -1)
                    find_all_hor_paths(root_tag, 0)

                    new_all_paths = copy.copy(all_paths)

                    doc = ShingleBased.Document(new_all_paths)
                    doc_list.append(doc)

                    del all_paths[:]
                    """

                    html_files_path.append(os.path.join(top_dir1, html_file))
                    #except Exception:
                    #   print(html_file + ' Exp')


    distance_matrix = []

    i = 0
    j = 0
    for doci in doc_list:
        temp_dist = []
        for docj in doc_list:
            dist = calculate_distance(doci, docj)
            temp_dist.append(dist)
            print str(i) + ' -- ' + str(j)
            j +=1
        distance_matrix.append(temp_dist)
        j = 0
        i += 1

    for a in distance_matrix:
        print(a)


