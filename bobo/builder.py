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
import script_loader
import generator

g_builder = None

class Builder(object):
    """The core class, contains the whole building information.
    """
    def __init__(self, root_dir, work_dir):
        self.root_dir = root_dir
        self.work_dir = work_dir
        self.script_loader = script_loader.get_loader(self.root_dir)
        self.script_loader.load_root_file()
        self.script_loader.set_work_dir(self.work_dir)
        logging.debug('init done')
        console.succ('init done')
        
        self.ordered_targets = []  # targets in order decreased by dependencies
        self.rules = []
        
    def build(self):
        console.info('building ...')
        logging.debug('')
        targets = self.script_loader.load_build_file(self.work_dir)
        # TODO(bin3): calculate ordered_targets
        ordered_targets = targets
        
        self.gen_head_rules()
        for i in range(len(ordered_targets)-1, -1, -1):
            self.gen_rules(ordered_targets[i])
        self.write_rules()
        logging.debug('targets: %s' % ordered_targets)
        console.succ('build done')
        
    def test(self, target):
        console.info('test')
        logging.debug('')
        
    def run(self, args):
        logging.debug('args: %s' % args)
        
        os.chdir(self.root_dir)
        
        if args.cmd == 'build':
            self.build()
        elif args.cmd == 'test':
            self.test()
        else:
            logging.error('Invalid command: %s' % args.cmd)
        
        self.exec_scons()
            
    def set_work_dir(self, work_dir):
        self.work_dir = work_dir
        
    def get_work_dir(self):
        return self.work_dir
        
    def gen_head_rules(self):
        self.rules.append(generator.HEAD_RULES)
        
    def gen_rules(self, target):
        self.rules += target.gen_rules()
        
    def write_rules(self):
        sconstruct_file = fileutil.get_sconstruct_file(self.root_dir)
        with open(sconstruct_file , 'w') as outf:
            outf.writelines(self.rules)
            
    def exec_scons(self):
        #options
        scons_options = '--duplicate=soft-copy --cache-show'
        #scons_options += ' -j %s' % options.jobs
        scons_options += ' -j 8'
        #if options.keep_going:
        #    scons_options += ' -k'
    
        logging.info('scons_options: %s' % scons_options)
        logging.info('cwd: %s' % os.getcwd())
    #    exit(1)
        
        p = subprocess.Popen("scons %s" % scons_options, shell=True)
        try:
            p.wait()
            if p.returncode:
                console.error("building failed")
                return p.returncode
        except:  # KeyboardInterrupt
            return 1
        console.succ("building done")
        return 0
        
    # ----------- Not used right now
    def register(self, target):
        """Register a target"""
        self._target_map[target.key] = target
        
    def find_deps(self, target):
        for dep in target.deps:
            self.find_dep(target, dep)
            
    def find_dep(self, target, dep_path):
        """Find the dependent target for a given target
        """
        sep = dep_path.rfind(fileutil.PATH_SEPARATOR)
        if sep == -1:
            (dep_dir, name) = ('.', dep_path)
        else:
            (dep_dir, name) = (dep_path[:sep], dep_path[sep+1:])
        if len(name) == 0:
            console.abort('Failed to find dependent target %s, the path(%s) is '
                        'invalid' % (dep_path,  target.key))
        
def main():
    logging.debug('Welcome to Bobo!')
    parser = argparse.ArgumentParser(description='Bobo, an easy to use '
        'building tool.')
    parser.add_argument('cmd', help='Command: build, test or run')
    args = parser.parse_args()
    
    abs_work_dir = os.getcwd()
    console.info('Working directory: %s' % abs_work_dir)
    root_dir = fileutil.find_root_dir(abs_work_dir)
    console.info('Root directory: %s' % root_dir)
    work_dir = fileutil.get_work_dir(root_dir, abs_work_dir)
    
    g_builder = Builder(root_dir, work_dir)
    g_builder.run(args)
    
if __name__ == '__main__':
    main()