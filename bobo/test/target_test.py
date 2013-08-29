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
#@date        2013-8-28

import unittest

from bobo import target

class CcLibraryTest(unittest.TestCase):
    def test_gen_rules(self):
        t = target.CcLibrary(work_dir='example/util', name='util', srcs=['util.cpp', 'common.cpp'])
        rules = t.gen_rules()
        self.assertEqual(3, len(rules), 'rules: %s' % rules)

class CcBinaryTest(unittest.TestCase):
    def test_gen_rules(self):
        t = target.CcBinary(work_dir='example/util_main', name='util', srcs=['util.cpp', 'common.cpp'])
        rules = t.gen_rules()
        self.assertEqual(3, len(rules), 'rules: %s' % rules)
        self.assertEqual('env_example__util_main__util = top_env.Clone()\n', rules[0])
        self.assertEqual("example__util_main__util = env_example__util_main__util.Program('build/example/util_main/util', ['build/example/util_main/util.cpp', 'build/example/util_main/common.cpp'])\n", rules[1])
        self.assertEqual('\n', rules[2])
        
        t = target.CcBinary(work_dir='example/util_main', name='util', srcs='util.cpp')
        rules = t.gen_rules()
        self.assertEqual(3, len(rules), 'rules: %s' % rules)
        self.assertEqual('env_example__util_main__util = top_env.Clone()\n', rules[0])
        self.assertEqual("example__util_main__util = env_example__util_main__util.Program('build/example/util_main/util', ['build/example/util_main/util.cpp'])\n", rules[1])
        self.assertEqual('\n', rules[2])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_gen_rules']
    unittest.main()