#!/usr/bin/python
from file_parser import FileParser

def gen_test(path):
  gen_sh(path + "/test.sh", [
    "#!/bin/bash",
    "if b; then",
    "  r",
    "fi",
  ])

def gen_build(path):
  gen_sh(path + "/build.sh", [
    "#!/bin/bash",
    "g++ -std=c++0x -I. test.cpp",
  ])

def gen_run(path):
  gen_sh(path + "/run.sh", [
    "#!/bin/bash",
    "./a.out",
  ])

def gen_problem(path, formatted_file_name):
  if os.path.isfile(path + "/test.sh"):
    print "already generated " + path
    return 1
  gen_test(path)
  gen_build(path)
  gen_run(path)
  file_parser = FileParser(formatted_file_name)
