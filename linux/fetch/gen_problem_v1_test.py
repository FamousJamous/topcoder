from gen_problem_v1 import *
from test_utils import *

def srm416_d1_l1():
  clean_up_testing_outputs()
  gen_problem("testing/outputs", "testing/inputs/srm416.d1.l1.formatted")
  expect_file_v1("testing/outputs/next_number.h", "testing/expected/srm416/d1/l1/next_number.h")
  expect_file_v1("testing/outputs/test.cpp", "testing/expected/srm416/d1/l1/test.cpp")
  clean_up_testing_outputs()

def srm416_d2_l3():
  clean_up_testing_outputs()
  gen_problem("testing/outputs", "testing/inputs/srm416.d2.l3.formatted")
  expect_file_v1("testing/outputs/dancing_couples.h", "testing/expected/srm416/d2/l3/dancing_couples.h")
  expect_file_v1("testing/outputs/test.cpp", "testing/expected/srm416/d2/l3/test.cpp")
  clean_up_testing_outputs()

if "__main__" == __name__:
  srm416_d1_l1()
  srm416_d2_l3()
