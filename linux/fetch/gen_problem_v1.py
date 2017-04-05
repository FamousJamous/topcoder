from file_parser import FileParser
from gen_cpp import gen_cpp
from gen_h import gen_h
from gen_shs import gen_shs

def gen_problem(path, formatted_file_name):
  gen_shs(path)
  file_parser = FileParser(formatted_file_name)
  gen_h(path, file_parser)
  gen_cpp(path, file_parser)
