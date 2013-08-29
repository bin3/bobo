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
#@author     Binson Zhang <bin183cs@gmail.com>
#@date        2013-8-26

import unittest
import os

from bobo import loader

class Test(unittest.TestCase):
    def setUp(self):
        root_dir = os.getcwd()
        self.loader = loader.get_loader(root_dir)

    def test_load_build_file(self):
        targets = self.loader.load_build_file('data/cc_library')
        self.assertEqual(1, len(targets))
        self.assertEqual('adder', targets[0].name)
        
    def test_get_abs_work_dir(self):
        self.assertEqual(self.loader.root_dir + '/myproj/util',
                         self.loader.get_abs_work_dir('/myproj/util'))
        self.assertEqual(self.loader.root_dir + '/myproj/util',
                         self.loader.get_abs_work_dir('myproj/util'))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()