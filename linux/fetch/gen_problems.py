#!/usr/bin/python
import os
from gen_problem import gen_problem
from gen_url import gen_url
from mkdir import mkdir

def gen_problems(srm_num, formatted_file_names, urls, srm_dir):
  div = 1
  level = 1
  div_dir = "%s/d%d" %(srm_dir, div)
  for formatted_file_name in formatted_file_names:
    mkdir(div_dir)
    level_dir = "%s/l%d" %(div_dir, level)
    mkdir(level_dir)
    gen_problem(level_dir, formatted_file_name)
    gen_url(level_dir, urls[div][level])
    level += 1
    if 4 == level:
      div += 1
      level = 1
      div_dir = "%s/d%d" %(srm_dir, div)
