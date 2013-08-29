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
#@date        2013-8-25

import distutils.core

args = {
        'name': 'bobo',
        'version': '0.0.1',
        'description': 'An easy to use building tool',
        'long_description': 'Bobo is an easy to use building tool.',
        'author': 'Binson Zhang',
        'author_email': 'bin183cs@gmail.com',
        'url': 'https://github.com/bin3/trowel',
        'platforms': ['Linux', 'Unix', 'Mac OS-X', 'Windows'],
        'license': 'Apache v2',
        'packages': ['bobo'],
        'scripts': ['scripts/bb'],
}

distutils.core.setup(**args)
