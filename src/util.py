#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import yaml
import zipfile as zf


def get_root_path():
    ROOT_DIR = 'dashboard_sample'
    return re.sub(f'{ROOT_DIR}.*', ROOT_DIR, os.path.abspath('.'))


def get_paths():
    root_path = get_root_path()
    with open(f'{root_path}/src/path.yaml', 'r') as f:
        path_dict = yaml.safe_load(f)

    for key in path_dict:
        path = path_dict[key]
        path_dict[key] = f'{root_path}/{path}'
    return path_dict


def unzip(fname, output_path):
    with zf.ZipFile(fname) as z:
        z.extractall(output_path)
