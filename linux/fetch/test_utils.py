import os
import itertools

def expect_eq(exp, val):
  if exp != val:
    print "exp {} doesn't equal val {}".format(exp, val)
    assert(False)

def print_with_line_marked(lines, marked_line):
  line_num = 0
  for line in lines:
    line = line[:len(line) - 1]
    if line_num == marked_line:
      print ">>> '{}'".format(line)
    else:
      print "'{}'".format(line)
    line_num += 1

def append_newlines(lines):
  res = []
  for line in lines:
    res.append("{}\n".format(line))
  return res

def expect_file_v1(file_name, exp_file_name):
  exp_lines = open(exp_file_name).readlines()
  res_lines = open(file_name).readlines()
  line_num = 0
  for res, exp in itertools.izip(res_lines, exp_lines):
    if res != exp:
      print "unexpected contents for {}.".format(file_name)
      print "expected lines:"
      print_with_line_marked(exp_lines, line_num)
      print "actual lines:"
      print_with_line_marked(res_lines, line_num)
      break
    line_num += 1

def expect_file(file_name, exp_lines):
  exp_lines = append_newlines(exp_lines)
  res_lines = open(file_name).readlines()
  line_num = 0
  for res, exp in itertools.izip(res_lines, exp_lines):
    if res != exp:
      print "unexpected contents for {}.".format(file_name)
      print "expected lines:"
      print_with_line_marked(exp_lines, line_num)
      print "actual lines:"
      print_with_line_marked(res_lines, line_num)
      break
    line_num += 1

def clean_up_testing_outputs():
  outputs_path = "testing/outputs"
  for file_name in os.listdir(outputs_path):
    os.remove("{}/{}".format(outputs_path, file_name))
