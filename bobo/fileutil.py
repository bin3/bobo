# -*- coding: utf-8 -*-
#
# Copyright(C) 2013 Binson Zhang.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#

__author__ = 'Binson Zhang <bin183cs@gmail.com>'
__date__ = '2013-8-25'

import os

import console

BUILD_ROOT_FILE = 'BUILD_ROOT'
BUILD_FILE = 'BUILD'

PATH_SEPARATOR = '/'

ROOT_PREFIX = '/'
WORKSPACE_PREFIX = '//'
EXTERNAL_PREFIX = '#'

def find_root_dir(working_dir):
    """ Find the first directory which has the TROWEL_ROOT file.
    
    Search from the bottom to up.
    """
    root_dir = os.path.normpath(working_dir)
    while root_dir != PATH_SEPARATOR:
        root_file = os.path.join(root_dir, BUILD_ROOT_FILE)
        if os.path.isfile(root_file):
            return root_dir
        root_dir = os.path.dirname(root_dir)
    console.abort('Failed to find the root directory for working directory %s, '
        'which has the file %s. ' % (working_dir, BUILD_ROOT_FILE))

def get_root_file(root_dir):    
    return os.path.join(root_dir, BUILD_ROOT_FILE)

def get_build_file(abs_work_dir):    
    return os.path.join(abs_work_dir, BUILD_FILE)

def get_work_dir(root_dir, abs_work_dir):
    """get work_dir from root_dir and abs_work_dir
    e.g. '/home/ws/', '/home/ws/example/util' -> 'example/util'
    """
    root_dir = os.path.normpath(root_dir)
    abs_work_dir = os.path.normpath(abs_work_dir)
    assert abs_work_dir.startswith(root_dir)
    return abs_work_dir[len(root_dir)+1:]

def get_work_dir_from_path(path):
    return os.path.dirname(path)

def get_sconstruct_file(root_dir):
    return os.path.join(root_dir, 'SConstruct')

def norm_path(path):
    """normalize path from user input 
    e.g. '/util/adder' -> 'util/adder'
    """
    if path.startswith(WORKSPACE_PREFIX):
        # TODO(bin3): impl
        console.abort('Not implemented')
    elif path.startswith(ROOT_PREFIX):
        return path[len(ROOT_PREFIX):]
    return path
