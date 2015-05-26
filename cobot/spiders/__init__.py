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

import os

SITES = os.path.join(os.getcwd(), 'sites')
denied_extension = ['jpg', 'jpeg', 'png', 'doc', 'docx', 'xls', 'xlsx', 'pdf', 'txt', 'ppt', 'pptx']


def is_allowed(filename):
    for ext in denied_extension:
        if filename.endswith(ext):
            return False
    return True


def create_site_dir(dir_name):
    print('spiders.__init__: %s' % os.getcwd())
    dir_path = os.path.join(SITES, dir_name)
    if not os.path.exists(dir_path):
        try:
            os.mkdir(dir_path, 0755)
            return dir_path
        except IOError:
            print('Site directory error!!')
    else:
        raise Exception('Site is exist!!')
