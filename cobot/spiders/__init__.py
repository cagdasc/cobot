# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import os

SITES = os.path.join(os.getcwd(), 'sites')
denied_extension = ['jpg', 'jpeg', 'png', 'doc', 'docx', 'xls', 'xlsx', 'pdf']


def is_allowed(filename):
    for ext in denied_extension:
        if filename.endswith(ext):
            return False
    return True


def create_site_dir(dir_name):
    dir_path = os.path.join(SITES, dir_name)
    if not os.path.exists(dir_path):
        try:
            os.mkdir(dir_path, 0755)
            return dir_path
        except IOError:
            print('Site directory error!!')
    else:
        raise Exception('Site is exist!!')
