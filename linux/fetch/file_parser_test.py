from file_parser import *
from test_utils import *

def main():
  file_parser = FileParser("testing/inputs/srm416.d1.l1.formatted")
  expect_eq("NextNumber", file_parser.class_name())
  expect_eq(Signature(IntType(), "getNextNumber", [Param("N", IntType())]),
            file_parser.signature())
  expect_eq([
    Example(0, [1717], 1718),
    Example(1, [4], 8),
    Example(2, [7], 11),
    Example(3, [12], 17),
    Example(4, [555555], 555557)],
    file_parser.examples())

if "__main__" == __name__:
  main()
