import re

class Type(object):
  def __eq__(self, other):
    return self.__str__() == other.__str__()

  def __ne__(self, other):
    return not self.__eq__(other)

  def __str__(self):
    return "wtf"

class IntValParser(object):
  def parse(self, val_str):
    self._val = int(val_str)
    return True

  def val(self):
    return self._val

class IntType(Type):
  def __str__(self):
    return "int"

  def create_val_parser(self):
    return IntValParser()

def remove_front(rem, line):
  return line[len(rem):].strip()

def parse_type(type_str):
  if "int" == type_str:
    return IntType()
  return None

class Param(object):
  def __init__(self, name, type_):
    self._name = name
    self._type_ = type_

  def name(self):
    return self._name

  def type_(self):
    return self._type_

  def __eq__(self, other):
    return self.name() == other.name() and self.type_() == other.type_()

  def __ne__(self, other):
    return not self.__eq__(other)

def parse_param(param_str):
  [type_str, name] = param_str.strip().split(" ")
  return Param(name, parse_type(type_str))

def parse_params(params_str):
  return [parse_param(param_str) for param_str in params_str.split(",")]

class Signature(object):
  def __init__(self, returns, method_name, params):
    self._returns = returns
    self._method_name = method_name
    self._params = params

  def __eq__(self, other):
    return self.returns() == other.returns() and self.method_name() == other.method_name() and self.params() == other.params()

  def __ne__(self, other):
    return not self.__eq__(other)

  def returns(self):
    return self._returns

  def method_name(self):
    return self._method_name

  def params(self):
    return self._params

def parse_signature(signature_str):
  res = re.search(r"([a-zA-Z<>]*) ([a-zA-Z0-9]*)\((.*)\)", signature_str)
  [returns_str, method_name, params_str] = res.groups()
  return Signature(parse_type(returns_str),
                   method_name,
                   parse_params(params_str))

class Example(object):
  def __init__(self, num, param_vals, returns_val):
    self._num = num
    self._param_vals = param_vals
    self._returns_val = returns_val

  def __eq__(self, other):
    return self.num() == other.num() and self.param_vals() == other.param_vals() and self.returns_val() == other.returns_val()

  def __ne__(self, other):
    return not self.__eq__(other)

  def __str__(self):
    return "num: {}, param_vals: {}, returns_val: {}".format(
      self.num(), self.param_vals(), self.returns_val())

  def num(self):
    return self._num

  def param_vals(self):
    return self._param_vals

  def returns_val(self):
    return self._returns_val

EX_PARSER_NUM = 0
EX_PARSER_PARAM_VALS = 1
EX_PARSER_RETURNS_VAL = 2
EX_PARSER_DONE = 3

class ExampleParser(object):
  def __init__(self, num, returns, params):
    self._num = num
    self._returns = returns
    self._params = params
    self._params_i = 0
    self._val_parser = params[0].type_().create_val_parser()
    self._param_vals = []
    self._state = EX_PARSER_NUM

  def parse(self, line):
    if EX_PARSER_NUM == self._state:
      self._parse_num(line)
    elif EX_PARSER_PARAM_VALS == self._state:
      self._parse_param_vals(line)
    elif EX_PARSER_RETURNS_VAL == self._state:
      self._parse_returns_val(line)
    return EX_PARSER_DONE == self._state

  def _parse_num(self, line):
    if not line.startswith("{})".format(self._num)):
      return
    self._state = EX_PARSER_PARAM_VALS

  def _parse_param_vals(self, line):
    if not self._val_parser.parse(line):
      return
    self._param_vals.append(self._val_parser.val())
    self._params_i += 1
    if len(self._params) == self._params_i:
      self._state = EX_PARSER_RETURNS_VAL
      self._val_parser = self._returns.create_val_parser()
    else:
      self._val_parser = self._params[self._params_i].type_().create_val_parser()

  def _parse_returns_val(self, line):
    if line.startswith("Returns:"):
      line = remove_front("Returns:", line)
    if not self._val_parser.parse(line):
      return
    self._example = Example(self._num, self._param_vals, self._val_parser.val())
    self._state = EX_PARSER_DONE

  def example(self):
    return self._example

class ExamplesParser(object):
  def __init__(self, returns, params):
    self._num = 0
    self._returns = returns
    self._params = params
    self._init_example()
    self._examples = []

  def __eq__(self, other):
    return self.examples() == other.examples()

  def __ne__(self, other):
    return not self.__eq__(other)

  def parse(self, line):
    if self._example_parser.parse(line):
      self._examples.append(self._example_parser.example())
      self._num += 1
      self._init_example()

  def _init_example(self):
    self._example_parser = ExampleParser(self._num, self._returns, self._params)

  def examples(self):
    return self._examples

FILE_PARSER_CLASS = 0
FILE_PARSER_SIGNATURE = 1
FILE_PARSER_EXAMPLES = 2

class FileParser(object):
  def __init__(self, file_name):
    self._state = FILE_PARSER_CLASS
    self._examples_parser = None
    for line in open(file_name):
      self._parse_line(line)

  def _parse_line(self, line):
    line = line.strip()
    if "" == line:
      return
    if FILE_PARSER_CLASS == self._state:
      self._parse_class(line)
    elif FILE_PARSER_SIGNATURE == self._state:
      self._parse_signature(line)
    elif FILE_PARSER_EXAMPLES == self._state:
      self._parse_examples(line)

  def _parse_class(self, line):
    if not line.startswith("Class:"):
      return
    self._class_name = remove_front("Class:", line)
    self._state = FILE_PARSER_SIGNATURE

  def _parse_signature(self, line):
    if not line.startswith("Method signature:"):
      return
    self._signature = parse_signature(remove_front("Method signature:", line))
    self._state = FILE_PARSER_EXAMPLES

  def _parse_examples(self, line):
    if not self._examples_parser:
      self._examples_parser = ExamplesParser(self._signature.returns(),
                                             self._signature.params())
    self._examples_parser.parse(line)

  def class_name(self):
    return self._class_name

  def signature(self):
    return self._signature

  def examples(self):
    return self._examples_parser.examples()
