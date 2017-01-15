from gen_problem_v1 import *
from test_utils import *

if "__main__" == __name__:
  clean_up_testing_outputs()
  gen_problem("testing/outputs", "testing/inputs/srm416.d1.l1.formatted")
  expect_file("testing/outputs/test.sh", [
    "#!/bin/bash",
    "if b; then",
    "  r",
    "fi",
    "",
  ])
  expect_file("testing/outputs/build.sh", [
    "#!/bin/bash",
    "g++ -std=c++0x -I. test.cpp",
    "",
  ])
  expect_file("testing/outputs/run.sh", [
    "#!/bin/bash",
    "./a.out",
    "",
  ])
  expect_file("testing/outputs/next_number.h", [
    "#ifndef NEXT_NUMBER_H",
    "#define NEXT_NUMBER_H",
    "",
    "struct NextNumber {",
    "",
    "int getNextNumber(int N) {",
    "  return int();",
    "}",
    "",
    "};",
    "",
    "#endif",
    "",
  ])
  expect_file("testing/outputs/test.cpp", [
    "#include \"next_number.h\"",
    "#include <assert.h>",
    "#include <iostream.h>",
    "",
    "void test(int N, int exp) {",
    "  int res = NextNumber().getNextNumber(N);",
    "  if (res != exp) {",
    "    cerr << \"exp \" << exp << \" res \" << res << endl;",
    "    assert(0);",
    "  }",
    "}",
    "",
    "int main() {",
    "  int N0 = 1717;",
    "  int exp0 = 1718;",
    "  test(N0, exp0);",
    "",
    "  int N1 = 4;",
    "  int exp1 = 8;",
    "  test(N1, exp1);",
    "",
    "  int N2 = 7;",
    "  int exp2 = 11;",
    "  test(N2, exp2);",
    "",
    "  int N3 = 12;",
    "  int exp3 = 17;",
    "  test(N3, exp3);",
    "",
    "  int N4 = 555555;",
    "  int exp4 = 555557;",
    "  test(N4, exp4);",
    "",
    "  return 0;",
    "}",
  ])
  clean_up_testing_outputs()
