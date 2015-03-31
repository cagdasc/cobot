__author__ = 'cagdascaglak'

import os
from colyzer import SITES

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

