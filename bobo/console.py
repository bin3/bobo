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

import sys
import os

color_enabled = (sys.stdout.isatty() and
                 os.environ['TERM'] not in ('emacs', 'dumb'))

def info(msg):
    msg = '[bobo info] ' + msg
    if color_enabled:
        # blue
        msg = '\033[34m' + msg + '\033[0m'
    print >>sys.stderr, msg

def succ(msg):
    msg = '[bobo info] ' + msg
    if color_enabled:
        # green
        msg = '\033[36m' + msg + '\033[0m'
    print >>sys.stderr, msg
    
def warn(msg):
    msg = '[bobo warn] ' + msg
    if color_enabled:
        # yellow
        msg = '\033[33m' + msg + '\033[0m'
    print >>sys.stderr, msg

def error(msg):
    msg = '[bobo error] ' + msg
    if color_enabled:
        # red
        msg = '\033[31m' + msg + '\033[0m'
    print >>sys.stderr, msg
    
def abort(msg, code=1):
    error(msg)
    sys.exit(code)
