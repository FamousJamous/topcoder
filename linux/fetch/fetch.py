#!/usr/bin/python
import sys
from format_problems import format_problems
from gen_problems import gen_problems
from get_srm_url import get_srm_url
from get_problem_urls import get_problem_urls
    
def main():
  if 4 != len(sys.argv):
    print "usage: %s <srm num> <data dir> <dest dir>" %(sys.argv[0])
    return
  srm_num = float(sys.argv[1])
  data_dir = sys.argv[2]
  srm_url = get_srm_url(srm_num, data_dir)
  print "srm url " + srm_url
  problem_urls = get_problem_urls(srm_num, srm_url, data_dir)
  formatted_file_names = format_problems(srm_num, data_dir, problem_urls)
  dest_dir = sys.argv[3]
  gen_problems(srm_num, formatted_file_names, problem_urls, dest_dir)

if "__main__" == __name__:
  main()
