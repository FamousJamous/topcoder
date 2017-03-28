from gen_shs import *
from test_utils import *

if "__main__" == __name__:
  clean_up_testing_outputs()
  gen_shs("testing/outputs")
  expect_file_v1("testing/outputs/test.sh", "testing/expected/test.sh")
  expect_file_v1("testing/outputs/build.sh", "testing/expected/build.sh")
  expect_file_v1("testing/outputs/run.sh", "testing/expected/run.sh")
  clean_up_testing_outputs()
