import datetime
import os
import sys

class ValType(object):
  def add_libs(self, lib_name_set, libs):
    None

  def pre_val(self, val, var_name):
    return ""

  def wrap_val(self, val, var_name):
    return str(val)

  def get_assert(self):
    return "res == exp"

class IntType(ValType):
  def __str__(self):
    return "int"

  def parse(self, val_str):
    return [True, int(val_str)]

class LongType(ValType):
  def __str__(self):
    return "long long"

  def parse(self, val_str):
    return [True, long(val_str)]

class DoubleType(ValType):
  def __str__(self):
    return "double"

  def parse(self, val_str):
    return [True, float(val_str)]

  def get_assert(self):
    return "abs(res - exp) < 1e-9"

class StringType(ValType):
  def __str__(self):
    return "string"

  def parse(self, val_str):
    return [True, val_str]

  def add_libs(self, lib_name_set, libs):
    lib_name_set.add("string")

class VectType(ValType):
  def __init__(self, type_str):
    self._contains = parse_type(type_str[:len(type_str) - 2])

  def __str__(self):
    return "vector<" + self._contains.__str__() + ">"

  def parse(self, val_str):
    if val_str.endswith('}'):
      val_str = val_str[1:len(val_str) - 1]
      return [True, [self._contains.parse(val_elem.strip())[1] for val_elem in val_str.split(",")]]
    else:
      return [False, None]

  def add_libs(self, lib_name_set, libs):
    if "vector" not in lib_name_set:
      lib_name_set.add("vector")
      libs.append(VectorLib())
    self._contains.add_libs(lib_name_set, libs)

  def pre_val(self, val, var_name):
    return "  %s %s_ar[] = {%s};\n" %(str(self._contains), var_name,
                                      ", ".join([self._contains.wrap_val(elem, var_name) for elem in val]))

  def wrap_val(self, val, var_name):
    return "aToV(%s_ar)" %(var_name)

class VectorLib:
  def create_helpers_str(self):
    return "\n".join([
      "template <typename T>",
      "ostream& operator<<(ostream& os, const vector<T>& v) {",
      "  for (int i = 0, n = v.size(); i < n; ++i) {",
      "    os << i << \": \" << v[i] << endl;",
      "  }",
      "  return os;",
      "}",
      "",
      "template <>",
      "ostream& operator<<(ostream& os, const vector<int>& v) {",
      "  if (v.empty()) {",
      "    return os;",
      "  }",
      "  os << v[0];",
      "  for (int i = 1, n = v.size(); i < n; ++i) {",
      "    os << ' ' << v[i];",
      "  }",
      "  return os;",
      "}",
      "",
      "template <int n, typename T>",
      "vector<T> aToV(T (&a)[n]) {",
      "  vector<T> v;",
      "  for (int i = 0; i < n; ++i) {",
      "    v.push_back(a[i]);",
      "  }",
      "  return v;",
      "}",
    ])

class Libs:
  def __init__(self, types):
    lib_name_set = set(["cassert", "iostream"])
    self.__libs = []
    for type in types:
      type.add_libs(lib_name_set, self.__libs)
    self.__lib_names = list(lib_name_set)
    self.__lib_names.sort()

  def create_includes_str(self):
    return "\n".join(["#include <%s>" %(lib_name) for lib_name in self.__lib_names])

  def create_helpers_str(self):
    return "\n".join(lib.create_helpers_str() for lib in self.__libs)

def parse_type(type_str):
  if type_str.endswith("[]"):
    return VectType(type_str)
  if type_str.startswith("int"):
    return IntType()
  elif type_str.startswith("long"):
    return LongType()
  elif type_str.startswith("String"):
    return StringType()
  elif type_str.startswith("double"):
    return DoubleType()
  else:
    raise type_str

def parse_types(types_str):
  return [parse_type(type_str) for type_str in types_str.split(", ")]

def remove_str(in_str, remove):
  return in_str[len(remove):].strip()

def parse_param_names(signature):
  params = signature[signature.find('(') + 1:signature.find(')')]
  return [param[param.rfind(' ') + 1:] for param in params.split(",")]

class ValParser:
  def __init__(self, type):
    self.__type = type
    self.reset()

  def parse(self, val_str):
    self.__val_str += val_str
    [done, val] = self.__type.parse(self.__val_str)
    if done:
      self.__done = True
      self.__val = val

  def done(self):
    return self.__done

  def get_val(self):
    return self.__val

  def reset(self):
    self.__done = False
    self.__val_str = ""

EX_PARSE_INITIAL = 0
EX_PARSE_PARAMS = 1
EX_PARSE_RETURNS = 2

def create_param_val_str(param, name, val, num):
  var_name = "%s%d" %(name, num)
  return "%s"\
         "  %s %s = %s;" %(param.pre_val(val, var_name),
                           str(param),
                           var_name,
                           param.wrap_val(val, var_name))

class Example:
  def __init__(self, num, param_vals, returns_val):
    self.__num = num
    self.__param_vals = param_vals
    self.__returns_val = returns_val

  def __str__(self):
    return "\n".join([
      "ex %d" %(self.__num),
      "params " + ", ".join([str(val) for val in self.__param_vals]),
      "returns " + str(self.__returns_val),
    ])

  def create_test_str(self, parser):
    return "\n".join([
      self.__create_param_vals_str(parser),
      self.__create_exp_str(parser),
      self.__create_test_call(parser),
    ])

  def __create_param_vals_str(self, parser):
    num = self.__num
    params = parser.get_params()
    names = parser.get_param_names()
    vals = self.__param_vals
    return "\n".join([
      create_param_val_str(param, name, val, num) for param, name, val in zip(params, names, vals)
    ])

  def __create_exp_str(self, parser):
    arg_name = "exp%d" %(self.__num)
    returns = parser.get_returns()
    returns_val = self.__returns_val
    return "%s"\
           "  %s %s = %s;" %(returns.pre_val(returns_val, arg_name),
                             str(returns), arg_name,
                             returns.wrap_val(returns_val, arg_name))

  def __create_test_call(self, parser):
    num = self.__num
    return "  test(%s, %s);" %(", ".join(["%s%d" %(name, num) for name in parser.get_param_names()]),
                               "exp%d" %(num))

class ExamplesParser:
  def __init__(self, params, returns):
    self.__ex_num = 0
    self.__param_parsers = [ValParser(param) for param in params]
    self.__returns_parser = ValParser(returns)
    self.__examples = []
    self.__reset_example()

  def __reset_example(self):
    self.__param_parsers_i = 0
    self.__state = EX_PARSE_INITIAL
    self.__returns_parser.reset()
    for param_parser in self.__param_parsers:
      param_parser.reset()

  def parse(self, line):
    if EX_PARSE_INITIAL == self.__state:
      self.__initial(line)
    elif EX_PARSE_PARAMS == self.__state:
      self.__params(line)
    elif EX_PARSE_RETURNS == self.__state:
      self.__returns(line)
    else:
      raise self.__state

  def __initial(self, line):
    if "%d)" % self.__ex_num == line:
      self.__state = EX_PARSE_PARAMS

  def __params(self, line):
    param_parser = self.__param_parsers[self.__param_parsers_i]
    param_parser.parse(line)
    if param_parser.done():
      self.__param_parsers_i += 1
    if len(self.__param_parsers) == self.__param_parsers_i:
      self.__state = EX_PARSE_RETURNS

  def __returns(self, line):
    if line.startswith("Returns:"):
      line = remove_str(line, "Returns:")
    self.__returns_parser.parse(line)
    if self.__returns_parser.done():
      param_vals = [param_parser.get_val() for param_parser in self.__param_parsers]
      returns_val = self.__returns_parser.get_val()
      self.__examples.append(Example(self.__ex_num, param_vals, returns_val))
      self.__reset_example()
      self.__ex_num +=1

  def get_examples(self):
    return self.__examples

STATE_INITIAL = 0
STATE_DEFINITION = 1
STATE_EXAMPLES = 2
STATE_DONE = 3

class Parser:
  def __init__(self, test_name):
    self.__state = STATE_INITIAL
    for line in open(test_name + ".in").readlines():
      self.__parse_line(line)

  def __parse_line(self, line):
    line = line.strip()
    if "" == line:
      return
    if (STATE_INITIAL == self.__state):
      self.__initial(line)
    if (STATE_DEFINITION == self.__state):
      self.__definition(line)
    if (STATE_EXAMPLES == self.__state):
      self.__examples(line)
    if (STATE_DONE == self.__state):
      self.__done(line)

  def __initial(self, line):
    if "Definition" == line:
      self.__state = STATE_DEFINITION

  def __definition(self, line):
    if "Examples" == line:
      self.__state = STATE_EXAMPLES
      self.__examples_parser = ExamplesParser(self.__params, self.__returns)
      return
    if line.startswith("Class:"):
      self.__class_name = remove_str(line, "Class:")
    elif line.startswith("Method:"):
      self.__method_name = remove_str(line, "Method:")
    elif line.startswith("Parameters:"):
      self.__params = parse_types(remove_str(line, "Parameters:"))
    elif line.startswith("Returns:"):
      self.__returns = parse_type(remove_str(line, "Returns:"))
    elif line.startswith("Method signature:"):
      self.__param_names = parse_param_names(remove_str(line, "Method signature:"))

  def __examples(self, line):
    if "This problem statement is the exclusive and proprietary property of "\
       "TopCoder, Inc. Any unauthorized use or reproduction of this information"\
       " without the prior written consent of TopCoder, Inc. is strictly "\
       "prohibited. (c)2010, TopCoder, Inc. All rights reserved." == line:
      self.__state = STATE_DONE
      return
    self.__examples_parser.parse(line)

  def __done(self, line):
    return

  def get_class_name(self):
    return self.__class_name

  def get_method_name(self):
    return self.__method_name

  def get_params(self):
    return self.__params

  def get_returns(self):
    return self.__returns

  def get_param_names(self):
    return self.__param_names

  def get_examples(self):
    return self.__examples_parser.get_examples()

def create_params_str(parser):
  params = parser.get_params()
  names = parser.get_param_names()
  return ", ".join([str(param) + " " + name for param, name in zip(params, names)])

def create_helpers_file_name(test_name):
  return test_name + ".helpers.h"

def gen_helpers(test_name, libs):
  helpers = open(create_helpers_file_name(test_name), "w")
  helpers.write("\n".join([
    "#ifndef %s_HELPERS_H" %(test_name),
    "#define %s_HELPERS_H" %(test_name),
    "",
    libs.create_includes_str(),
    "",
    "using namespace std;",
    "",
    libs.create_helpers_str(),
    "",
    "#endif",
  ]))

def create_header_file_name(test_name):
  return test_name + ".h"

def create_test_function(parser):
  return "\n".join([
    "void test(%s, %s exp) {" %(create_params_str(parser), str(parser.get_returns())),
    "\n".join([
      "  cout << \"%s: \" << %s << endl;" %(name, name)
      for name in parser.get_param_names()
    ]),
    "  %s res = %s().%s(%s);" %(str(parser.get_returns()),
                                parser.get_class_name(),
                                parser.get_method_name(),
                                ", ".join(parser.get_param_names())),
    "  cout << \"res: \" << res << \" exp: \" << exp << endl << endl;",
    "  assert(%s);" %(parser.get_returns().get_assert()),
    "}",
  ])

def create_function(parser):
  return "\n".join([
    "%s %s(%s) {" %(str(parser.get_returns()),
                    parser.get_method_name(),
                    create_params_str(parser)),
    "  return %s();" %(str(parser.get_returns())),
    "}",
  ])

def gen_header(test_name, parser, libs):
  header = open(create_header_file_name(test_name), "w")
  header.write("\n".join([
    "#ifndef %s_H" %(parser.get_class_name().upper()),
    "#define %s_H" %(parser.get_class_name().upper()),
    "",
    "#include \"%s\"" %(create_helpers_file_name(test_name)),
    "",
    libs.create_includes_str(),
    "",
    "using namespace std;",
    "",
    "struct %s {" %(parser.get_class_name()),
    "",
    create_function(parser),
    "",
    "};",
    "",
    create_test_function(parser),
    "",
    "#endif"
  ]))

def gen_main(test_name, parser):
  main = open(create_main_file_name(test_name), "w")
  main.write("\n".join([
    "#include \"%s\"" %(create_header_file_name(test_name)),
    "",
    "int main() {",
    "\n\n".join([example.create_test_str(parser) for example in parser.get_examples()]),
    "",
    "  cout << \"start time: %s\" << endl;" %(datetime.datetime.now()),
    "",
    "  return 0;",
    "}",
  ]))

def create_bat_file_name(test_name):
  return "t.bat"

def gen_bat(test_name):
  bat = open(create_bat_file_name(test_name), "w")
  bat.write("\n".join([
    "bcc32 %s.cpp" %(test_name),
    test_name,
  ]))

def create_main_file_name(test_name):
  return test_name + ".cpp"

def already_generated(test_name):
  return False
  return os.path.isfile(create_main_file_name(test_name))

def main():
  if 2 != len(sys.argv):
    print "usage: %s <test name>" %(sys.argv[0])
    return 1
  test_name = sys.argv[1]
  if already_generated(test_name):
    print "already generated %s" %(test_name)
    return 1
  parser = Parser(test_name)
  libs = Libs(parser.get_params() + [parser.get_returns()])
  gen_helpers(test_name, libs)
  gen_header(test_name, parser, libs)
  gen_main(test_name, parser)
  gen_bat(test_name)

if __name__ == "__main__":
  main()
