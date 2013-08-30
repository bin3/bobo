#!/usr/bin/env python
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
import generator
import fileutil

TOP_ENV = 'top_env'
BUILD_DIR = 'build'

NAME_SEP = '__'
ENV_PREFIX = 'env_'

def to_list(x):
    if isinstance(x, list):
        return x
    else:
        return [x]

def remove_prefix(s, prefix):
    if (s.startswith(prefix)):
        return s[len(prefix):]
    else:
        return s

def quote(s):
    return "'%s'" % s

class Target(object):
    """Target is the unit building block.
    """
    def __init__(self, 
                 work_dir,
                 name,
                 deps=[],
                 roots=[]):
        """
        deps:
        e.g. 
        current dir: glog
        BUILD_ROOT: /glog/glog
        workspace: //3rd/glog/glog
        external: #glog
        """
        console.info('building target: %s' % name)
        self.work_dir = work_dir
        self.name = name
        self.deps = to_list(deps)
        self.roots = to_list(roots)
        
        self.path = os.path.join(self.work_dir, self.name)
        self.full_name = self.path.replace(os.sep, NAME_SEP)
        self.env = ENV_PREFIX + self.full_name
        self.dep_paths = self.norm_deps(self.deps)
        self.all_dep_paths = []
        
    def gen_rules(self):
        return []
    
    def full_name(self):
        return os.path.join(self.work_dir, self.name)
    
    def norm_work_dir(self, work_dir):
        """normalize work_dir
        e.g. '/example/util' -> 'example/util'
        """
        if work_dir.starts_with(fileutil.ROOT_PREFIX):
            return remove_prefix(self.work_dir, fileutil.ROOT_PREFIX)
        else:
            return work_dir
            
    def norm_deps(self, deps):
        paths = []
        for dep in deps:
            if self.in_cur_dir(dep):
                dep = os.path.join(self.work_dir, dep)
            else:
                dep = fileutil.norm_path(dep)
            paths.append(dep)
        return paths
                
        
    def in_cur_dir(self, dep):
        if not dep.startswith(fileutil.ROOT_PREFIX) and not dep.startswith(fileutil.EXTERNAL_PREFIX):
            return True
        return False
    
    def __str__(self):
        return 'key: %s, deps: %s, roots: %s' % (self.key, self.deps, self.roots)
    
    def __repl__(self):
        return self.__str__()
    
class SrcsTarget(Target):    
    """Target with srcs
    """
    def __init__(self, 
                 work_dir,
                 name,
                 srcs,
                 deps=[],
                 roots=[]):
        Target.__init__(self, work_dir, name, deps, roots)
        self.srcs = to_list(srcs)
        self.builder = None
    
    def gen_rules(self):
        rules = []
        build_srcs = []
        for src in self.srcs:
            build_srcs.append(quote(os.path.join(generator.BUILD_DIR, self.work_dir, src)))
        build_target = quote(os.path.join(generator.BUILD_DIR, self.path))
        rules.append('%s = %s.Clone()\n' % (self.env, TOP_ENV))
        rules.append('%s = %s.%s(%s, [%s])\n' % \
                     (self.full_name, self.env, self.builder, build_target, ', '.join(build_srcs)))
        rules.append('\n')
        return rules
    
class CcLibrary(SrcsTarget):    
    """cc_library
    """
    def __init__(self, 
                 work_dir,
                 name,
                 srcs,
                 deps=[],
                 roots=[]):
        SrcsTarget.__init__(self, work_dir, name, srcs, deps, roots)
        self.builder = 'StaticLibrary'

class CcBinary(SrcsTarget):    
    """cc_binary
    """
    def __init__(self, 
                 work_dir,
                 name,
                 srcs,
                 deps=[],
                 roots=[]):
        SrcsTarget.__init__(self, work_dir, name, srcs, deps, roots)
        self.builder = 'Program'
