#!/usr/bin/python
import sys
from format_problems import format_problems
from gen_problems import gen_problems
from get_srm_url import get_srm_url
from get_problem_urls import get_problem_urls
    
def main():
  if 2 != len(sys.argv):
    print "usage: %s <srm num>" %(sys.argv[0])
    return
  srm_num = float(sys.argv[1])
  srm_url = get_srm_url(srm_num)
  print "srm url " + srm_url
  problem_urls = get_problem_urls(srm_num, srm_url)
  formatted_file_names = format_problems(srm_num, problem_urls)
  gen_problems(srm_num, formatted_file_names, problem_urls)

if "__main__" == __name__:
  main()
