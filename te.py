import sys

import tc

STATE_PRE = 0
STATE_IN = 1
STATE_IN_NOT_ARGS = 2
STATE_IN_PAST_ARGS = 4

def get_arg_type(arg):
  if tc.is_string(arg):
    return "string"
  if tc.is_int(arg):
    return "int"
  if tc.is_float(arg):
    return "double"
  if tc.is_vect(arg):
    tokens = arg[1:].split(',')
    return get_arg_type(tokens[0].strip())
  else:
    print "wtf"
    return None

def get_arg_type_extra(arg):
  if tc.is_vect(arg):
    return "[]"
  return ""

def parse_case(line, test_num, out):
  state = STATE_IN_NOT_ARGS
  arg_num = 0
  for token in line.split('\t'):
    if "" == token.strip():
      continue
    if STATE_IN_NOT_ARGS == state:
      for arg in [ arg.strip() for arg in token.split(",") ]:
        out.write("  %s ae%d_%d%s = %s;\n" %(get_arg_type(arg), test_num, arg_num, get_arg_type_extra(arg), arg))
        arg_num += 1
      state = STATE_IN_PAST_ARGS
    elif STATE_IN_PAST_ARGS == state:
      exp = token.strip()
      out.write("  %s ee%d%s = %s;\n" %(get_arg_type(exp), test_num, get_arg_type_extra(arg), exp))
      break
  out.write("  test(%s, ee%d);\n\n" %(", ".join([ "ae%d_%d" %(test_num, i) for i in range(arg_num) ]), test_num))

def main():
  if 2 != len(sys.argv):
    print "usage: %s <extra problems>" %(sys.argv[0])
    return 1
  state = STATE_PRE
  test_num = 0
  level = sys.argv[1]
  out = open(level + ".extra.cpp", "w")
  for line in open(level + ".extra").readlines():
    line = line.strip()
    if "" == line:
      continue
    if STATE_PRE == state:
      if "Test Arguments" == line[:len("Test Arguments")]:
        state = STATE_IN
    elif STATE_IN == state:
      if "SITEMAP" == line[:len("SITEMAP")]:
        break
      parse_case(line, test_num, out)
      test_num += 1

if __name__ == "__main__":
  main()
