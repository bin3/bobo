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
import logging

import console
import generator
import fileutil
import logutil

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
    def __init__(self, path):
        self.path = path
        self.name = path
        self.full_name = path
        self.dep_paths = []
        self.all_dep_targets = []
        
    def gen_rules(self):
        """generate scons rules for this target
        """
        return []
    
    def get_build_name(self):
        """return the name for building
        """
        return self.full_name
    
    def __hash__(self):
        return self.path.__hash__()
    
class ExternalTarget(Target):
    """External target, do not need to build it
    """
    def __init__(self, path):
        Target.__init__(self, path)
        self.name = fileutil.get_exteranl_name(path)
    
    def get_build_name(self):
        return quote(self.name)
    
class LocalTarget(Target):
    """Local target, need to build it
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
        console.info('Loaded target: %s' % name)
        self.work_dir = work_dir
        self.name = name
        self.deps = to_list(deps)
        self.roots = to_list(roots)
        
        self.path = os.path.join(self.work_dir, self.name)
        self.full_name = self.path.replace(os.sep, NAME_SEP)
        self.env = ENV_PREFIX + self.full_name
        self.dep_paths = self.norm_deps(self.deps)
        self.all_dep_targets = []
        self.rules = []
        
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
    
    def add_deps(self, target):
        self.all_dep_targets.extend(target.all_dep_targets)
        self.all_dep_targets.append(target)
        
    def names_str(self, targets):
        names = []
        for t in targets:
            names.append(t.get_build_name())
        return ', '.join(names)
    
    def split_deps(self):
        """split all_dep_targets to lib_deps and other_deps
        """
        lib_deps = []
        other_deps = []
        for t in self.all_dep_targets:
            if isinstance(t, ExternalTarget) or isinstance(t, CcLibrary) or \
            isinstance(t, ProtoLibrary):
                lib_deps.append(t)
            else:
                other_deps.append(t)
        logging.debug('lib_deps: %s' % lib_deps)
        logging.debug('other_deps: %s' % other_deps)
        return (lib_deps, other_deps)
    
    def gen_build_target(self):
        return quote(os.path.join(generator.BUILD_DIR, self.path))
        
    def in_cur_dir(self, dep):
        if not dep.startswith(fileutil.ROOT_PREFIX) and not dep.startswith(fileutil.EXTERNAL_PREFIX):
            return True
        return False
    
    def gen_env_rule(self):
        self.rules.append('%s = %s.Clone()\n' % (self.env, TOP_ENV))
        
    def gen_depend_rules(self, deps):
        for dep in deps:
            if not isinstance(dep, ExternalTarget):
                self.rules.append('%s.Depends(%s, %s)\n' % (self.env, self.get_build_name(), dep.get_build_name()))
    
    def __str__(self):
        return 'key: %s, deps: %s, roots: %s' % (self.key, self.deps, self.roots)
    
    def __repl__(self):
        return self.__str__()
    
class SrcsTarget(LocalTarget):    
    """Target with srcs
    """
    def __init__(self, 
                 work_dir,
                 name,
                 srcs,
                 deps=[],
                 roots=[]):
        LocalTarget.__init__(self, work_dir, name, deps, roots)
        self.srcs = to_list(srcs)
        self.builder = None
        
    def gen_build_srcs(self):
        build_srcs = []
        for src in self.srcs:
            build_srcs.append(quote(os.path.join(generator.BUILD_DIR, self.work_dir, src)))
        return ', '.join(build_srcs)
    
    
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
        
    def gen_rules(self):
        self.gen_env_rule()
        self.rules.append('%s = %s.StaticLibrary(%s, [%s])\n' % \
                     (self.full_name, self.env, 
                      self.gen_build_target(), 
                      self.gen_build_srcs()))
        self.gen_depend_rules(self.all_dep_targets)
        self.rules.append('\n')
        return self.rules

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

    def gen_rules(self):
        self.gen_env_rule()
        (lib_deps, other_deps) = self.split_deps()
        self.rules.append('%s = %s.Program(%s, [%s], LIBS=[%s])\n' % \
                     (self.full_name, self.env, 
                      self.gen_build_target(), 
                      self.gen_build_srcs(),
                      self.names_str(lib_deps)))
        self.gen_depend_rules(other_deps)
        self.rules.append('\n')
        return self.rules

class CcTest(SrcsTarget):    
    """cc_test
    """
    def __init__(self, 
                 work_dir,
                 name,
                 srcs,
                 deps=[],
                 roots=[]):
        deps = to_list(deps)
        deps.extend(['#gtest', '#gtest_main'])
        SrcsTarget.__init__(self, work_dir, name, srcs, deps, roots)

    def gen_rules(self):
        self.gen_env_rule()
        (lib_deps, other_deps) = self.split_deps()
        self.rules.append('%s = %s.Program(%s, [%s], LIBS=[%s])\n' % \
                     (self.full_name, self.env, 
                      self.gen_build_target(), 
                      self.gen_build_srcs(),
                      self.names_str(lib_deps)))
        self.gen_depend_rules(other_deps)
        self.rules.append('\n')
        return self.rules
    
class ProtoLibrary(SrcsTarget):    
    """proto_library
    """
    PROTO_SUFFIX = '.proto'
    CC_SUFFIX = '.pb.cc'
    
    def __init__(self, 
                 work_dir,
                 name,
                 srcs,
                 deps=[],
                 roots=[]):
        deps = to_list(deps)
        deps.append('#protobuf')
        SrcsTarget.__init__(self, work_dir, name, srcs, deps, roots)

    def gen_rules(self):
        self.gen_env_rule()
        self.rules.append("%s.Proto('NO_TARGET', [%s])\n" % \
                     (self.env, self.gen_build_srcs()))
        self.rules.append('%s = %s.StaticLibrary(%s, [%s])\n' % \
                          (self.full_name, self.env,
                          self.gen_build_target(), 
                          self.gen_cc_srcs()))
        self.gen_depend_rules(self.all_dep_targets)
        self.rules.append('\n')
        return self.rules
    
    def gen_cc_srcs(self):
        cc_srcs = []
        for src in self.srcs:
            if src.endswith(ProtoLibrary.PROTO_SUFFIX):
                src = src[:-len(ProtoLibrary.PROTO_SUFFIX)] + ProtoLibrary.CC_SUFFIX
            cc_srcs.append(quote(os.path.join(generator.BUILD_DIR, self.work_dir, src)))
        return ', '.join(cc_srcs)
    