def create_include_strs(signature, additional):
  libs = additional + signature.returns().get_libs()
  for param in signature.params():
    libs += param.type_().get_libs()
  libs = list(set(libs))
  libs.sort()
  return "\n".join(["#include <{}>".format(lib) for lib in libs])
