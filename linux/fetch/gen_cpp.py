import itertools
from create_include_strs import create_include_strs
from create_header_name import create_header_name

def create_test_params_str(signature):
  return ", ".join([
    "{} {}".format(param.type_(), param.name()) for param in signature.params()
  ] + ["{} exp".format(signature.returns())])

def create_call_func_params_str(params, suffix):
  return ", ".join(["{}{}".format(param.name(), suffix) for param in params])

def create_call_func_str(file_parser):
  signature = file_parser.signature()
  return "{}().{}({})".format(
    file_parser.class_name(),
    signature.method_name(),
    create_call_func_params_str(signature.params(), suffix = ""))

def create_test_func_str(file_parser):
  signature = file_parser.signature()
  return "\n".join([
    "void test({}) {{".format(create_test_params_str(signature)),
    "  {} res = {};".format(signature.returns(), create_call_func_str(file_parser)),
    "  if (res != exp) {",
    "    cerr << \"exp \" << exp << \" res \" << res << endl;",
    "    assert(0);",
    "  }",
    "}",
  ])

def create_test_case_params_str(params, example):
  num = example.num()
  return "\n".join([
    "  {} {}{} = {};".format(param.type_(),
                             param.name(),
                             num,
                             val) for param, val in itertools.izip(params,
                                                                   example.param_val_strs())
  ])

def create_test_case_returns_str(returns, example):
  return "  {} exp{} = {};".format(returns,
                                   example.num(),
                                   example.returns_val_str())

def create_test_case_call_str(signature, num):
  return "  test({}, exp{});".format(
    create_call_func_params_str(signature.params(), num), num)

def create_test_case_str(signature, example):
  return "\n".join([
    create_test_case_params_str(signature.params(), example),
    create_test_case_returns_str(signature.returns(), example),
    create_test_case_call_str(signature, example.num())
  ])

def create_test_cases_str(file_parser):
  return "\n\n".join([
    create_test_case_str(file_parser.signature(), example) for example in file_parser.examples()
  ])

def gen_cpp(path, file_parser):
  open("{}/test.cpp".format(path), "w").write(
  "\n".join([
    "#include \"{}\"".format(create_header_name(file_parser.class_name())),
    create_include_strs(file_parser.signature(), ["cassert", "iostream"]),
    "",
    "namespace {",
    "",
    "using namespace std;",
    "",
    create_test_func_str(file_parser),
    "",
    "} // namespace",
    "",
    "int main() {",
    create_test_cases_str(file_parser),
    "",
    "  return 0;",
    "}",
    "",
  ]))
