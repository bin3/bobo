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
__date__ = '2013-8-27'

TOP_ENV = 'top_env'
BUILD_DIR = 'build'

NAME_SEP = '__'
ENV_PREFIX = 'env_'

# colors
colors = {}
colors['red']    = '\033[31m'
colors['green']  = '\033[32m'
colors['yellow'] = '\033[33m'
colors['blue']   = '\033[34m'
colors['purple'] = '\033[1;35m'
colors['cyan']   = '\033[36m'
colors['white']  = '\033[37m'
colors['gray']   = '\033[38m'
colors['end']    = '\033[0m'

HEAD_RULES = """import os

top_env = Environment(ENV=os.environ)

BUILD_DIR = 'build'
top_env.Append(CPPPATH='.')
top_env.Append(LIBPATH=BUILD_DIR)

VariantDir(BUILD_DIR, '.', duplicate=0) 
"""

def gen_builder_rules_str():
	PROTO_BUILDER = '__proto_builder'
	rules = []
	rules.append("%s = Builder(action = 'protoc -I.  -I`dirname $SOURCE` --cpp_out=. $SOURCE')" % PROTO_BUILDER)
	rules.append("top_env.Append(BUILDERS = {'Proto': %s})" % PROTO_BUILDER)
	rules.append('')
	return '\n'.join(rules)

def gen_output_control_rules_str():
	compile_str = '%sCompiling $SOURCE%s' % (colors['yellow'], colors['end'])
	build_lib_str = '%sBuilding $TARGET%s' % (colors['purple'], colors['end'])
	ranlib_str = '%sranlib $TARGET%s' % (colors['purple'], colors['end'])
	build_bin_str = '%sBuilding $TARGET%s' % (colors['red'], colors['end'])
	rules_str = "top_env.Append(\n\
		CCCOMSTR = '%s',\n\
		CXXCOMSTR = '%s',\n\
		SHCCCOMSTR = '%s',\n\
		SHCXXCOMSTR = '%s',\n\
		ARCOMSTR = '%s',\n\
		RANLIBCOMSTR = '%s',\n\
		LINKCOMSTR = '%s',\n\
		SHLINKCOMSTR = '%s'\n)\n\n" \
		% (compile_str, compile_str, compile_str, compile_str, build_lib_str, ranlib_str, build_bin_str, build_bin_str)
	return rules_str

def gen_head_rules_str():
	rules = []
	rules.append(HEAD_RULES)
	rules.append(gen_builder_rules_str())
	rules.append(gen_output_control_rules_str())
	return '\n'.join(rules)
