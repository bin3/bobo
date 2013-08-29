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

import traceback
import os

import target
import fileutil
import console

g_loaded_targets = []
_loader = None

def cc_library(name,
               srcs=[],
               deps=[],
               roots=[]):
    t = target.CcLibrary(_loader.get_work_dir(), name, srcs, deps, roots)
    _loader.load_target(t)

def cc_binary(name,
        srcs=[],
        deps=[],
        roots=[]):
    t = target.CcBinary(_loader.get_work_dir(), name, srcs, deps, roots)
    _loader.load_target(t)

def cc_test():
    pass

def workerspace():
    pass

def cc_config():
    pass

class ScriptLoader(object):
    """Used to load BUILD_ROOT and BUILD scripts.
    """
    def __init__(self, root_dir):
        """root_dir is an absolutely path
        """
        self.root_dir = root_dir
        self.work_dir = '/'
        self.loaded_targets = []
        
    def set_work_dir(self, work_dir):
        """work_dir is an relative path starts from root_dir
        """
        self.work_dir = work_dir
    
    def get_work_dir(self):
        return self.work_dir
        
    def get_abs_work_dir(self, work_dir):
        """Get the absolutely work dir
        """
        if work_dir.startswith(fileutil.PATH_SEPARATOR):
            return self.root_dir + work_dir
        return os.path.join(self.root_dir, work_dir)
        
    def load_target(self, target):
        self.loaded_targets.append(target)
        
    def load_root_file(self):
        """Load BUILD_ROOT.
        """
        root_file = fileutil.get_root_file(self.root_dir)
        try:
            execfile(root_file)
        except Exception, e:
            console.abort('Failed to parse root file %s.\nException: %s' 
                          % (root_file, e))
            
    def load_build_file(self, work_dir):
        """Load BUILD.
        """
        self.set_work_dir(work_dir)
        abs_work_dir = self.get_abs_work_dir(work_dir)
        build_file = fileutil.get_build_file(abs_work_dir)
        # clear loaded_targets before execfile 
        self.loaded_targets = []
        try:
            execfile(build_file)
        except Exception, e:
            traceback.print_exc(limit=10)
            console.abort('Failed to parse build file %s.\nException: %s' 
                          % (build_file, e))
        return self.loaded_targets

def get_loader(root_dir):
    """Get the global ScriptLoader
    """
    global _loader
    if (_loader is None):
        _loader = ScriptLoader(root_dir)
    return _loader
