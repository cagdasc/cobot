__author__ = 'cagdascaglak'

import os
from colyzer import SITES
from lxml import etree
import copy

real_paths = []


def find_real_paths(tag, tmp_list):
    tmp_list.append(tag.tag)
    if len(tag) != 0:
        for t in tag:
            find_real_paths(t, tmp_list)
    new_list = copy.copy(tmp_list)
    real_paths.append(new_list)
    if len(tmp_list) > 0:
        del tmp_list[len(tmp_list) - 1]
    return


def find_all_real_paths(tag):
    for t in tag:
        temp_list = []
        find_real_paths(t, temp_list)
        find_all_real_paths(t)

if __name__ == '__main__':

    html_files_path = []
    for top_dir0, sub_dirs0, files0 in os.walk(os.path.join(SITES)):
        for site_dir in sub_dirs0:
            for top_dir1, sub_dirs1, page_files in os.walk(os.path.join(top_dir0, site_dir)):
                for html_file in page_files:
                    """
                    with open(os.path.join(top_dir1, html_file)) as f:
                        html = f.read()
                    print(html)
                    break
                    """
                    html_files_path.append(os.path.join(top_dir1, html_file))

    tree = etree.parse("/Users/cagdascaglak/Desktop/default2.html", parser=etree.HTMLParser(remove_comments=True))
    # print(tree.getroot().tag)

    root_tag = tree.getroot()[1]

    find_all_real_paths(root_tag)
    for i in real_paths:
        print(i)