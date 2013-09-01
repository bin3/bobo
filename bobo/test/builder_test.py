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
#@date        2013-8-30

import unittest
import os

from bobo import builder

class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
    #def setUp(self):
        os.chdir('data')
        
    def test_cc_library(self):
        builder.main('build cc_library'.split()) 

    def test_cc_binary(self):
        builder.main('build example'.split()) 

    def test_cc_proto(self):
        builder.main('build proto'.split()) 

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()