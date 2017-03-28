import os
import re
from create_header_name import create_header_name

def create_include_guard(class_name):
 temp = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', class_name)
 return "{}_H".format(re.sub('([a-z0-9])([A-Z])', r'\1_\2', temp).upper())

def create_params_str(params):
  return ", ".join(["{} {}".format(param.type_(),
                                   param.name()) for param in params])

def create_signature_str(signature):
  return "{} {}({})".format(signature.returns(),
                            signature.method_name(),
                            create_params_str(signature.params()))

def gen_h(path, file_parser):
  class_name = file_parser.class_name()
  file_path = "{}/{}".format(path, create_header_name(class_name))
  if os.path.isfile(file_path):
    print "already generated {}".format(file_path)
    return
  include_guard = create_include_guard(class_name)
  returns_type = str(file_parser.signature().returns())
  open(file_path, "w").write(
    "\n".join([
      "#ifndef {}".format(include_guard),
      "#define {}".format(include_guard),
      "",
      "struct {} {{".format(class_name),
      "",
      "{} {{".format(create_signature_str(file_parser.signature())),
      "  return {}();".format(returns_type),
      "}",
      "",
      "};",
      "",
      "#endif",
      "",
    ])
  )

