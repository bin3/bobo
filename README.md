bobo
====

Bobo is an easy to use building tool inspired by [blade](https://github.com/chen3feng/typhoon-blade).

Dependencies
----
* python
* scons

Install
----
```
sudo ./setup.py install
```
Usage
----
* Create the `BUILD_ROOT` file in the workspace directory.

```
cd <WORKSPACE_DIR>
touch BUILD_ROOT
```
* Edit a `BUILD` file in a directory project, which is a sub-directory of the worksapce directory.

```
cd <PROJECT_DIR>
vim BUILD
```
A BUILD file may be like this:

```
proto_library(
    name = 'example_proto',
    srcs = 'example.proto',
)

cc_library(
    name = 'example',
    srcs = 'example.cpp',
    deps = [
        'example_proto',
    ]
)

cc_test(
    name = 'example_test',
    srcs = 'example_test.cpp',
    deps = 'example',
)

cc_binary(
    name = 'example_main',
    srcs = 'main.cpp',
    deps = [
    	'example',
    	'/common/concurrency',
    	'//util/algorithm',
        '#glog',
    ],
    roots = [
    	'/subws/src/util',
    ]
)
```
* Run bb command.

```
bb build
```
Differences between bobo and blade
----
* bobo supports sub-workspace by `roots` option.
* bobo supports external libraries and headers by `libs` and `incs` options.
* bobo is under Apache V2 license, which is more friendly to users and developers.

Target types
----
* `cc_library`: build a library.
* `cc_binary`: build a binary.
* `cc_test`: build unittest binary based on `gtest`.
* `proto_library`: build a `protobuf` library.
