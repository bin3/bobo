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

import argparse
import logging
import os
import subprocess

import logutil
import fileutil
import console
import loader
import generator
import dependency
from target import ExternalTarget

g_builder = None

class Builder(object):
    """The core class, contains the whole building information.
    """
    def __init__(self, root_dir, work_dir):
        self.root_dir = root_dir
        self.work_dir = work_dir
        self.loader = loader.get_loader(self.root_dir)
        self.loader.load_root_file()
        self.loader.set_work_dir(self.work_dir)
        logging.debug('init done')
        
        self.sorted_targets = []  # targets in order decreased by dependencies
        self.rules = []
#        self.loaded_dirs = set()
#        self.target_map = {}
        
    def build(self):
        targets = self.loader.load_build_file(self.work_dir)
        self.load_all_deps(targets)
        
        analyzer = dependency.DependencyAnalyzer(targets, self.target_map)
        sorted_targets = analyzer.analyze()
            
        self.gen_head_rules()
        for t in sorted_targets:
            self.gen_rules(t)
        self.write_rules()
        logging.debug('targets: %s' % sorted_targets)
        
    def test(self, target):
        console.info('test')
        logging.debug('')
        
    def run(self, args):
        logging.debug('args: %s' % args)
        
        os.chdir(self.root_dir)
        
        if args.target != None:
            work_dir = os.path.join(self.work_dir, args.target)
            self.set_work_dir(work_dir)
        logging.debug(self.get_work_dir())
        
        if args.cmd == None or args.cmd == 'build' or args.cmd == 'b':
            self.build()
        elif args.cmd == 'test' or args.cmd == 't':
            self.test()
        else:
            console.error('Invalid command: %s' % args.cmd)

        console.succ('Init done')
        
        self.exec_scons()
            
    def set_work_dir(self, work_dir):
        self.work_dir = work_dir
        
    def get_work_dir(self):
        return self.work_dir
        
    def gen_head_rules(self):
        self.rules.append(generator.HEAD_RULES)
        self.rules.append(generator.gen_output_control_rules_str())
        
    def gen_rules(self, target):
        self.rules += target.gen_rules()
        
    def write_rules(self):
        sconstruct_file = fileutil.get_sconstruct_file(self.root_dir)
        with open(sconstruct_file , 'w') as outf:
            outf.writelines(self.rules)
        
    def load_all_deps(self, targets):
        """load all depended targets for given targets
        """
        self.target_map = {}
        for t in targets:
            self.register_target(t)
            
        self.loaded_deps = set()
        for t in targets:
            self.load_deps(t)
            
    def load_deps(self, target):
        """load depended targets for a given target
        """
        logging.debug('path=%s, dep_paths=%s' % (target.path, target.dep_paths))
        if target in self.loaded_deps: return
        self.loaded_deps.add(target)
         
        for path in target.dep_paths:
            dep_target = self.load_target(path)
            self.load_deps(dep_target)
            
    def has_target(self, path):
        return path in self.target_map
    
    def get_target(self, path):
        if path in self.target_map:
            return self.target_map[path]
        return None
    
    def register_target(self, target):
        self.target_map[target.path] = target
    
    def load_target(self, path):
        """load a target if necessary
        """
        if self.has_target(path):
            return self.get_target(path)
        
        if fileutil.is_external_path(path):
            # do not need to load BUILD file, just create a ExternalTarget 
            target = ExternalTarget(path)
            self.register_target(target)
            return target
        
        work_dir = fileutil.get_work_dir_from_path(path)
        targets = self.loader.load_build_file(work_dir)
        logging.debug('targets: %s' % targets)
        target = None
        for t in targets:
            self.register_target(t)
            logging.debug('t.path=%s' % t.path)
            if path == t.path:
                target = t
        if target == None:
            console.abort('No target %s found' % path)
        return target
                      
    def exec_scons(self):
        #options
        scons_options = ' --duplicate=soft-copy --cache-show -Q '
        #scons_options += ' -j %s' % options.jobs
        scons_options += ' -j 8 '
        #if options.keep_going:
        #    scons_options += ' -k'
    
        logging.debug('scons_options: %s' % scons_options)
        logging.debug('cwd: %s' % os.getcwd())
        
        p = subprocess.Popen("scons %s" % scons_options, shell=True)
        try:
            p.wait()
            if p.returncode:
                console.error("Building failed")
                return p.returncode
        except:  # KeyboardInterrupt
            return 1
        console.succ("Building done")
        return 0  
    
def main(args=None):
    logging.debug('Welcome to Bobo!')
    parser = argparse.ArgumentParser(description='Bobo, an easy to use '
        'building tool.')
    parser.add_argument('cmd', nargs='?', help='Command: build, test or run')
    parser.add_argument('target', nargs='?', help='Target: a target or a directory')
    args = parser.parse_args(args)
    
    abs_work_dir = os.getcwd()
    root_dir = fileutil.find_root_dir(abs_work_dir)
    console.info('Root directory: %s' % root_dir)
    console.info('Working directory: %s' % abs_work_dir)
    work_dir = fileutil.get_work_dir(root_dir, abs_work_dir)
    
    g_builder = Builder(root_dir, work_dir)
    g_builder.run(args)
    
if __name__ == '__main__':
    main()