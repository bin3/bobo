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
__date__ = '2013-8-30'

from collections import defaultdict

import console
import logutil
import logging

class DependencyAnalyzer(object):
    def __init__(self, targets, target_map):
        self.targets = targets
        self.target_map = target_map
        self.out_degs = {}
        self.in_nodes = defaultdict(list)
        self.built_paths = set()
        self.sorted_paths = []
        logging.debug('target_map: %s' % self.target_map)
    
    def analyze(self):
        """analyze dependency graph and return topological sorted targets
        """
        self._build_graph()
        self._topological_sort()
        return self._gen_sorted_targets()
    
    def _build(self, target):
        if target.path in self.built_paths: return
        self.built_paths.add(target.path)
        if len(target.dep_paths) == 0:
            self.sorted_paths.append(target.path)
            return
        self.out_degs[target.path] = len(target.dep_paths)
        for path in target.dep_paths:
            self.in_nodes[path].append(target.path)
            self._build(self.target_map[path])
            
    def _build_graph(self):
        for t in self.targets:
            self._build(t)
            
    def _topological_sort(self):
        i = 0
        while i < len(self.sorted_paths):
            cur = self.sorted_paths[i]
            cur_target = self.target_map[cur]
            for in_node in self.in_nodes[cur]:
                t = self.target_map[in_node]
                t.add_deps(cur_target)
                self.out_degs[in_node] -= 1
                if self.out_degs[in_node] == 0:
                    self.sorted_paths.append(in_node)
            i += 1
        # check dependency loop
        if sum(self.out_degs.values()) != 0:
            loop_paths = [path for path, deg in self.out_degs.items() if deg != 0]
            console.abort('Dependency loop exists: %s' % loop_paths)
    
    def _gen_sorted_targets(self):     
        sorted_targets = []
        for path in self.sorted_paths:
            sorted_targets.append(self.target_map[path])
        return sorted_targets
        