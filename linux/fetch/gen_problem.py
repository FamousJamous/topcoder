#!/usr/bin/python
from gen_sh import gen_sh
import datetime
import os
import re

def match_field(name, line):
  res = re.search(r"%s:\t(.*)" %(name), line)
  if res:
    return res.groups()[0]

class IntType():
  def __str__(self):
    return "int"

class DoubleType():
  def __str__(self):
    return "double"

class LongType():
  def __str__(self):
    return "long"

class StringType():
  def __str__(self):
    return "string"

class VectorType():
  def __init__(self, type_str):
    self._type = parse_type(type_str)

  def __str__(self):
    return "vector<%s>" %(self._type)

def parse_type(type_str):
  if type_str.endswith("[]"):
    return VectorType(type_str[:len(type_str) - 2])
  if "int" == type_str:
    return IntType()
  if "double" == type_str:
    return DoubleType()
  if "long" == type_str:
    return LongType()
  if "String" == type_str:
    return StringType()

class Param():
  def __init__(self, type_str, name):
    self._type = parse_type(type_str)
    self._name = name

  def __str__(self):
    return "%s %s" %(self._type, self._name)

  def get_name(self):
    return self._name

  def get_type(self):
    return self._type

def parse_param(param_str):
  [ type_str, name ] = param_str.split(" ")
  return Param(type_str, name)

def parse_params(params_str):
  params = []
  for param_str in params_str.split(", "):
    params.append(parse_param(param_str))
  return params

class Signature():
  def __init__(self, returns_str, name, params_str):
    self._returns = parse_type(returns_str)
    self._name = name
    self._params = parse_params(params_str)

  def __str__(self):
    return "%s %s(%s)" %(self._returns, self._name, ", ".join([str(param) for param in self._params]))

  def get_returns(self):
    return self._returns

  def get_name(self):
    return self._name

  def get_params(self):
    return self._params

def is_vect(t):
  return t.__str__().startswith("vector")
    
def parse_signature(signature_str):
  res = re.search("(\S+) (\S+)\((.*)\)", signature_str)
  [ returns_str, name, params_str ] = res.groups()
  return Signature(returns_str, name, params_str)

EX_GET_INPUTS = 0
EX_GET_OUTPUT = 1

class Example():
  def __init__(self, ex_lines, signature):
    self._inputs = []
    params = signature.get_params()
    pi = 0
    vect_str = ""
    state = EX_GET_INPUTS
    for line in ex_lines:
      line = line.strip()
      if line.startswith("Returns:"):
        state = EX_GET_OUTPUT
        line = line[len("Returns:"):].strip()
      if EX_GET_INPUTS == state:
        print line
        if is_vect(params[pi]):
          vect_str += line
          if line.endswith("}"):
            self._inputs.append(vect_str)
            vect_str = ""
            pi += 1
        else:
          self._inputs.append(line)
          pi +=1
      else:
        if is_vect(signature.get_returns()):
          vect_str += line
          if line.endswith("}"):
            self._output = vect_str[len("Returns: "):]
        else:
          self._output = line[len("Returns: "):]

  def __str__(self):
    return "inputs: %s, output: %s" %(", ".join(self._inputs), self._output)

  def get_output(self):
    return self._output

  def get_inputs(self):
    return self._inputs

def add_not_none(e, s):
  if e:
    s.add(e)

def header_from_type(_type):
  type_str = _type.__str__()
  if type_str.startswith("vector"):
    return "vector"
  if "string" == type_str:
    return "string"

def gen_include(header):
  return "#include <" + header + ">"

def gen_includes(signature, headers):
  headers = set(headers)
  add_not_none(header_from_type(signature.get_returns()), headers)
  for param in signature.get_params():
    add_not_none(header_from_type(param.get_type()), headers)
  headers = list(headers)
  headers.sort()
  return "\n".join([gen_include(header) for header in headers])

def gen_vector_helpers():
  return "\n".join([
    "template <typename T>",
    "ostream & operator<<(ostream & os, vector<T> const & v) {",
    "  for (auto e : v) {",
    "    os << e << endl;",
    "  }",
    "  return os;",
    "}",
    "",
    "template <>",
    "ostream & operator<<(ostream & os, vector<int> const & v) {",
    "  for (int i : v) {",
    "    os << i << \" \";",
    "  }",
    "  return os;",
    "}",
    "",
  ])

def gen_vector_cpp_helpers():
  return "\n".join([
    "template <int n, typename T>",
    "vector<T> aToV(T const (&ar)[n]) {",
    "  vector<T> v;",
    "  for (int i = 0; i < n; ++i) {",
    "    v.push_back(ar[i]);",
    "  }",
    "  return v;",
    "}",
  ])

def uses_vector(signature):
  for param in signature.get_params():
    if param.get_type().__str__().startswith("vector"):
      return True
  return signature.get_returns().__str__().startswith("vector")

def gen_helpers(signature):
  if uses_vector(signature):
    return gen_vector_helpers()
  return ""

def gen_test_func_sig(signature):
  inputs = ", ".join([param.__str__() for param in signature.get_params()])
  ret_type = signature.get_returns().__str__()
  return "void test(%s, %s exp)" %(inputs, ret_type)

def gen_pass_inputs(signature, suffix):
  return ", ".join([param.get_name() + suffix for param in signature.get_params()])

def gen_res(_class, signature):
  ret_type = signature.get_returns().__str__()
  func = signature.get_name()
  inputs = gen_pass_inputs(signature, "")
  return "  %s res = %s().%s(%s);" %(ret_type, _class, func, inputs)

def gen_assert(signature):
  if "double" == signature.get_returns().__str__():
    return "assert(abs(exp - res) < 1e-9);"
  return "assert(exp == res);"

def gen_test_func(_class, signature):
  return "\n".join([
    "%s {" %(gen_test_func_sig(signature)),
    "%s" %(gen_res(_class, signature)),
    "  cout << \"exp \" << exp << endl;",
    "  cout << \" res \" << res << endl;",
    "  %s" %(gen_assert(signature)),
    "}",
  ])

def gen_init_input(param, inp, num):
  return "  %s%d = %s;" %(param.__str__(), num, inp)

def gen_init_inputs(params, inputs, num):
  return "\n".join([gen_init_input(params[i], inputs[i], num) for i in range(0, len(params))])

def gen_example(signature, example, num):
  ret_type = signature.get_returns().__str__()
  return "\n".join([
    "%s" %(gen_init_inputs(signature.get_params(), example.get_inputs(), num)),
    "  %s exp%d = %s;" %(ret_type, num, example.get_output()),
    "  test(%s);" %(gen_pass_inputs(signature, str(num)) + ", exp%d" %(num)),
  ])

def gen_examples(signature, examples):
  num = 0
  example_strs = []
  for example in examples:
    example_strs.append(gen_example(signature, example, num))
    num += 1
  return "\n\n".join(example_strs)

def gen_print_time():
  return "  cout << \"start time %s\" << endl;" %(datetime.datetime.now())

def gen_print_input(param):
  return "  cout << \"%s \" << %s << endl;" %(param.get_name(), param.get_name())

def gen_print_inputs(signature):
  return "\n".join([gen_print_input(param) for param in signature.get_params()])

STATE_GET_CLASS = 0
STATE_GET_METHOD_SIGNATURE = 1
STATE_FIND_EXAMPLES = 2
STATE_GET_EXAMPLE = 3

class FileParser():
  def __init__(self, formatted):
    self._state = STATE_GET_CLASS
    for line in formatted:
      self._parse_line(line)

  def _parse_line(self, line):
    if STATE_GET_CLASS == self._state:
      self._get_class(line)
    elif STATE_GET_METHOD_SIGNATURE == self._state:
      self._get_method_signature(line)
    elif STATE_FIND_EXAMPLES == self._state:
      self._find_examples(line)
    elif STATE_GET_EXAMPLE == self._state:
      self._get_example(line)

  def _get_class(self, line):
    self._class = match_field("Class", line)
    if self._class:
      self._state = STATE_GET_METHOD_SIGNATURE 

  def _get_method_signature(self, line):
    method_signature = match_field("Method signature", line)
    if method_signature:
      self._signature = parse_signature(method_signature)
      self._ex_num = 0
      self._examples = []
      self._ex_lines = []
      self._state = STATE_FIND_EXAMPLES

  def _find_examples(self, line):
    if "%d)" %(self._ex_num) == line.strip():
      self._state = STATE_GET_EXAMPLE

  def _get_example(self, line):
    line = line.strip()
    if not line:
      return
    self._ex_lines.append(line)
    if line.startswith("Returns:"):
      self._ex_num += 1
      self._examples.append(Example(self._ex_lines, self._signature))
      self._ex_lines = []
      self._state = STATE_FIND_EXAMPLES

  def gen_h(self, path):
    _class = self._class
    h = open(path + "/" + _class + ".h", "w")
    define = "%s_H" %(_class.upper())
    signature = self._signature
    h.write("\n".join([
      "#ifndef " + define,
      "#define " + define,
      "",
      "%s" %(gen_includes(signature, ["iostream"])),
      "",
      "using namespace std;",
      "",
      "namespace {",
      "",
      "%s" %(gen_helpers(signature)),
      "} // namespace",
      "",
      "struct " + _class + " {",
      "",
      signature.__str__() + " {",
      "%s" %(gen_print_inputs(signature)),
      "  return %s();" %(signature.get_returns().__str__()),
      "}",
      "",
      "};",
      "",
      "#endif",
      "",
    ]))

  def gen_cpp(self, path):
    cpp = open(path + "/test.cpp", "w")
    _class = self._class
    signature = self._signature
    cpp.write("\n".join([
      "#include <" + _class + ".h>",
      "%s" %(gen_includes(signature, ["cassert"])),
      "",
      "using namespace std;",
      "",
      "namespace {",
      "",
      "%s" %(gen_test_func(_class, signature)),
      "",
      "} // namespace",
      "",
      "int main() {",
      "",
      "%s" %(gen_examples(signature, self._examples)),
      "",
      "%s" %(gen_print_time()),
      "",
      "  return 0;",
      "}",
    ]))

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

def already_generated(path):
  return os.path.isfile(path + "/test.sh")

def gen_problem(path, formatted_file_name):
  if already_generated(path):
    print "already generated " + path
    return 1
  gen_test(path)
  gen_build(path)
  gen_run(path)
  file_parser = FileParser(open(formatted_file_name))
  file_parser.gen_h(path)
  file_parser.gen_cpp(path)
