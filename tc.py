import datetime
import sys

IND = "  "

def is_string(string):
  return 2 <= len(string) and string.startswith('"') and string.endswith('"')

def is_int(string):
  try:
    int(string)
    return True
  except ValueError:
    return False

def is_float(string):
  try:
    float(string)
    return True
  except ValueError:
    return False

def is_vect(string):
  return string.startswith('{') and string.endswith('}')

class Var(object):

  def get_type(self):
    pass

  def get_type_suffix(self):
    return ""

  def get_func_type(self):
    return self.get_type()

  def get_val(self):
    pass

  def get_template_arg(self):
    pass

  def get_test_prefix(self):
    return ""
  
  def get_test_suffix(self, num):
    return ""

  def get_helpers(self):
    pass

  def get_os_helper(self):
    pass

  def get_helper_call(self, name):
    pass

class StrVar(Var):
  def __init__(self, string):
    self._string = string
  def get_type(self):
    return "string"
  def get_val(self):
    return self._string

class IntVar(Var):
  def __init__(self, i):
    self._i = i
  def get_type(self):
    return "int"
  def get_val(self):
    return str(self._i)

class FloatVar(Var):
  def __init__(self, f):
    self._f = f
  def get_type(self):
    return "double"
  def get_val(self):
    return str(self._f)

class VectVar(Var):
  def __init__(self, vect):
    self._vect = vect
    self._type = ""
    for elem in vect:
      self._type = elem.get_type()

  def get_type(self):
    return self._type 

  def get_type_suffix(self):
    return "[]"

  def get_func_type(self):
    return "vector<%s>" %(self._type)

  def get_val(self):
    strs = []
    for elem in self._vect:
      strs.append(elem.get_val())
    return "{ " + ", ".join(strs)+ " }";

  def get_template_arg(self):
    return "int n"

  def get_test_prefix(self):
    return "(&ar_"
  
  def get_test_suffix(self, num):
    return ")[n%d]" %(num)

  def get_helpers(self):
    type = self._type
    return [
        "\n".join([
          "template <int n>",
          "vector<%s> %s_aToV(%s (&a)[n]) {" %(type, type, type),
          "%svector<%s> v;" %(IND, type),
          "%sfor (int i = 0; i < n; ++i) {" %(IND),
          "%s%sv.push_back(a[i]);" %(IND, IND),
          "%s}" %(IND),
          "%sreturn v;" %(IND),
          "}",
          "",
        ]),
        "\n".join([
          "template <typename T>",
          "ostream & operator<<(ostream & os, vector<T> const & v) {",
          "%sos << endl;" %(IND),
          "%sfor (int i = 0, n = v.size(); i < n; ++i) os << i << \": \" << v[i] << endl;" %(IND),
          "%sreturn os;" %(IND),
          "}",
          "",
        ]),
        "\n".join([
          "template <>",
          "ostream & operator<<(ostream & os, vector<int> const & v) {",
          "%sfor (int i = 0, n = v.size(); i < n; ++i) os << v[i] << \" \";" %(IND),
          "%sreturn os;" %(IND),
          "}",
          "",
        ])
    ]

  def get_helper_call(self, name):
    return "vector<%s> %s = %s_aToV(ar_%s);\n" %(self._type, name, self._type, name)

def str_to_var(string):
  if is_string(string):
    return StrVar(string)
  if is_int(string):
    return IntVar(int(string))
  if is_float(string):
    return FloatVar(float(string))
  if is_vect(string):
    val = []
    for sub_str in string[1:len(string) - 1].split(","):
      sub_str = sub_str.strip()
      val.append(str_to_var(sub_str))
    return VectVar(val)
  else:
    print "wtf str_to_var"
    return 1

class SigType:
  def __init__(self, string):
    l = len(string)
    if "[]" == string[l - 2:]:
      inner = SigType(string[:l - 2])
      self._string = "vector<%s>" %(inner.get_str())
    elif "String" == string:
      self._string = "string"
    else:
      self._string = string

  def get_str(self):
    return self._string

class SigArg:
  def __init__(self, string):
    tokens = string.split(' ')
    self._sig_type = SigType(tokens[0])
    self._name = tokens[1]

  def get_str(self):
    return "%s %s" %(self._sig_type.get_str(), self._name)

  def get_name(self):
    return self._name

class Sig:
  def __init__(self, string):
    space = string.find(' ')
    self._ret = SigType(string[:space].strip())
    string = string[space + 1:]
    paren = string.find('(')
    self._name = string[:paren].strip()
    string = string[paren + 1:]
    args = []
    for arg_str in string.split(","):
      if arg_str.endswith(')'):
        arg_str = arg_str[:len(arg_str) - 1]
      args.append(SigArg(arg_str.strip()))
    self._args = args

  def get_str(self):
    arg_strs = []
    for arg in self._args:
      arg_strs.append(arg.get_str())
    return "%s %s(%s)" %(self._ret.get_str(), self._name, ", ".join(arg_strs))

  def get_print_inputs_str(self):
    arg_strs = []
    for arg in self._args:
      arg_strs.append("%scout << \"%s: \" << %s << endl;" %(IND, arg.get_name(), arg.get_name()))
    return "\n".join(arg_strs) + "\n"

  def get_name(self):
    return self._name

  def get_ret_str(self):
    return self._ret.get_str()

def add_template_arg(arg, template_arg_num , template_args):
  template_arg = arg.get_template_arg()
  if template_arg:
    template_args.append("%s%d" %(template_arg, template_arg_num))
    return template_arg_num + 1
  return template_arg_num

def get_void_test_arg(arg, arg_name, template_arg_num):
  return "%s %s%s%s" %(arg.get_type(), arg.get_test_prefix(), arg_name, arg.get_test_suffix(template_arg_num))

def write_helper_call(cpp, arg, arg_name):
  helper_call = arg.get_helper_call(arg_name)
  if helper_call:
    cpp.write("%s%s" %(IND, helper_call))

def add_if_not_none(dups, helpers, additional):
  if None == additional:
    return
  for helper in additional:
    if helper in dups:
      continue
    helpers.append(helper)
    dups.add(helper)

class Case:
  def __init__(self, num, args, exp):
    self._num = num
    self._args = args
    self._exp = exp

  def gen_func(self, cpp, sig):
    cpp.write("%s {\n" %(sig.get_str()))
    cpp.write(sig.get_print_inputs_str())
    cpp.write("%sreturn %s();\n" %(IND, sig.get_ret_str()))
    cpp.write("}\n\n")

  def gen_test_func(self, cpp, sig):
    template_args = []
    template_arg_num = 0
    arg_strs = []
    arg_num = 0
    arg_names = []
    for arg in self._args:
      arg_name = "a%d" %(arg_num)
      arg_strs.append(get_void_test_arg(arg, arg_name, template_arg_num))
      arg_num += 1
      arg_names.append(arg_name)
      template_arg_num = add_template_arg(arg, template_arg_num, template_args)
    exp_str = get_void_test_arg(self._exp, "exp", template_arg_num)
    template_arg_num = add_template_arg(self._exp, template_arg_num, template_args)
    if template_args:
      cpp.write("template <%s>\n" %(", ".join(template_args)))
    cpp.write("void test(%s) {\n" %(", ".join(arg_strs + [ exp_str ])))
    self.gen_helper_calls(cpp)
    cpp.write("%s%s res = %s(%s);\n" %(IND, self._exp.get_func_type(), sig.get_name(), ", ".join(arg_names)))
    cpp.write("%scout << \"exp: \" << exp << \", res: \" << res << endl;\n" %(IND))
    cpp.write("%sassert(exp == res);\n" %(IND, ))
    cpp.write("}\n")

  def gen_helpers(self, cpp):
    dups = set()
    helpers = []
    for arg in self._args + [ self._exp ]:
      add_if_not_none(dups, helpers, arg.get_helpers())
    for helper in helpers:
      cpp.write("%s\n" %(helper))

  def gen_helper_calls(self, cpp):
    arg_num = 0
    for arg in self._args:
      arg_name = "a%d" %(arg_num)
      arg_num += 1
      write_helper_call(cpp, arg, arg_name)
    write_helper_call(cpp, self._exp, "exp")

  def gen(self, cpp):
    arg_num = 0
    arg_names = []
    for arg in self._args:
      arg_name = "a%d_%d" %(self._num, arg_num)
      cpp.write("%s%s %s%s = %s;\n" %(IND, arg.get_type(), arg_name, arg.get_type_suffix(), arg.get_val()))
      arg_num += 1
      arg_names.append(arg_name)
    exp_name = "e%d" %(self._num)
    exp = self._exp
    cpp.write("%s%s %s%s = %s;\n" %(IND, exp.get_type(), exp_name, exp.get_type_suffix(), exp.get_val()));
    cpp.write("%stest(%s, %s);\n\n" %(IND, ", ".join(arg_names), exp_name))

STATE_SIGNATURE = 0
STATE_COMMENTS = 1
STATE_QUES = 2

class Tests:
  def __init__(self, file_name):
    self._cases = []

    RET_LEN = len("Returns:")
    SIG_KEY_LEN = len("Method signature:")

    state = STATE_SIGNATURE
    ques_num = 0
    ques_start = "%d)" %(ques_num)
    args = []
    string = ""

    for line in open(file_name).readlines():
      line = line.strip()
      if not line:
        continue
      if STATE_SIGNATURE == state:
        if "Method signature:" == line[:SIG_KEY_LEN]:
          self._sig = Sig(line[SIG_KEY_LEN + 1:].strip())
          state = STATE_COMMENTS
      elif STATE_COMMENTS == state:
        if ques_start == line:
          state = STATE_QUES
      elif STATE_QUES == state:
        if "Returns:" == line[:RET_LEN]:
          exp = str_to_var(line[RET_LEN + 1:])
          self._cases.append(Case(ques_num, args, exp))
          state = STATE_COMMENTS
          ques_num += 1
          ques_start = "%d)" %(ques_num)
          args = []
        else:
          if line.endswith(','):
            string += line
          elif string:
            string += line
            args.append(str_to_var(string))
            string = ""
          else:
            args.append(str_to_var(line))
      else:
        print "wtf"
        return 1

  def gen_helpers(self, cpp):
    self._cases[0].gen_helpers(cpp)

  def gen_helper_calls(self, cpp):
    self._cases[0].gen_helper_calls(cpp)

  def gen_func(self, cpp):
    self._cases[0].gen_func(cpp, self._sig)

  def gen_test_func(self, cpp):
    self._cases[0].gen_test_func(cpp, self._sig)

  def gen_cases(self, cpp):
    for case in self._cases:
      case.gen(cpp)

  def has_strings(self):
    return True
  
  def has_vectors(self):
    return True

def write_header(cpp, tests):
  includes = [ "cassert", "iostream" ]

  if tests.has_strings():
    includes.append("string")

  if tests.has_vectors():
    includes.append("vector")

  for include in includes:
    cpp.write("#include <%s>\n" %(include))

  cpp.write("\nusing namespace std;\n")

  cpp.write("\nnamespace {\n\n")

  tests.gen_helpers(cpp)
  tests.gen_func(cpp)
  tests.gen_test_func(cpp)

  cpp.write("\n} // namespace\n\n")

def write_print_time(cpp):
  cpp.write("%scout << \"start time %s\" << endl;\n" %(IND, datetime.datetime.now()))

def write_main(cpp, tests):
  cpp.write("int main() {\n")
  tests.gen_cases(cpp)
  write_print_time(cpp)
  cpp.write("%sreturn 0;\n" %(IND))
  cpp.write("}\n")

def gen_t(test_name):
  bat = open("t.bat", "w")
  bat.write("bcc32 -etest %s.cpp\n" %(test_name))
  bat.write("test")

def gen_b(test_name):
  bat = open("b.bat", "w")
  bat.write("bcc32 -etest %s.cpp\n" %(test_name))

def gen_main(test_name):
  cpp = open(test_name + ".cpp", "w")
  tests = Tests(test_name + ".in")
  write_header(cpp, tests)
  write_main(cpp, tests)

def main():
  if 2 != len(sys.argv):
    print "usage: %s <test name>" %(sys.argv[0])
    return 1
  test_name = sys.argv[1]
  gen_t(test_name)
  gen_b(test_name)
  gen_main(test_name)

if __name__ == "__main__":
  main()
