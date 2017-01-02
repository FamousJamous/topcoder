#!/usr/bin/python
from format_problems import format_problems
from gen_problems import gen_problems
from gen_url import gen_url
from get_srm_url import get_srm_url
from get_problem_urls import get_problem_urls
from mkdir import mkdir
import sys
    
def main():
  if 4 != len(sys.argv):
    print "usage: %s <srm num> <data dir> <dest dir>" %(sys.argv[0])
    return
  srm_num = float(sys.argv[1])
  data_dir = sys.argv[2]
  srm_url = get_srm_url(srm_num, data_dir)
  print "srm%d %s" %(srm_num, srm_url)
  dest_dir = sys.argv[3]
  srm_dir = "%s/srm%d" %(dest_dir, srm_num)
  mkdir(srm_dir)
  gen_url(srm_dir, srm_url)
  problem_urls = get_problem_urls(srm_num, srm_url, data_dir)
  formatted_file_names = format_problems(srm_num, data_dir, problem_urls)
  gen_problems(srm_num, formatted_file_names, problem_urls, srm_dir)

if "__main__" == __name__:
  main()
