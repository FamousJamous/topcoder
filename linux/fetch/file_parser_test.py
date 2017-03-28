from file_parser import *
from test_utils import *

def srm416_d1_l1():
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

def srm416_d2_l3():
  file_parser = FileParser("testing/inputs/srm416.d2.l3.formatted")
  expect_eq("DancingCouples", file_parser.class_name())
  expect_eq(Signature(IntType(), "countPairs", [Param("canDance", VectType(StringType())),
                                                Param("K", IntType())]),
            file_parser.signature())
  expect_eq([
    Example(0, [["YYYY", "YYYY", "YYYY"], 3], 24),
    Example(1, [["YYNN", "NYYN", "NNYY"], 3], 4),
    Example(2, [["YY", "YY", "YY"], 3], 0),
    Example(3, [["YYNNNN", "NYYNNN", "NNYYNN", "NNNYYN", "NNNNYY", "YNNNNY"], 3], 112)],
    file_parser.examples())

if "__main__" == __name__:
  srm416_d1_l1()
  srm416_d2_l3()
