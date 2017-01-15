from gen_sh import gen_sh

def gen_test(path):
  gen_sh(path + "/test.sh", [
    "#!/bin/bash",
    "if b; then",
    "  r",
    "fi",
    "",
  ])

def gen_build(path):
  gen_sh(path + "/build.sh", [
    "#!/bin/bash",
    "g++ -std=c++0x -I. test.cpp",
    "",
  ])

def gen_run(path):
  gen_sh(path + "/run.sh", [
    "#!/bin/bash",
    "./a.out",
    "",
  ])

def gen_shs(path):
  gen_test(path)
  gen_build(path)
  gen_run(path)
