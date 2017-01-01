#!/usr/bin/python
import re
from get_html_cached import get_html_cached

def get_problem_urls(srm_num, srm_url):
  div = 1
  level = 1
  file_name = "srm%d" %(srm_num)
  srm_html = get_html_cached(srm_url, file_name)
  problem_urls = { 1: { 1: "", 2: "", 3: "" }, 2: { 1: "", 2: "", 3: "" } }
  for line in srm_html:
    res = re.search(r'problem_statement(\S+)"', line)
    if not res:
      continue
    url = "https://community.topcoder.com/stat?c=problem_statement" + res.groups()[0]
    problem_urls[div][level] = url
    level += 1
    if 4 == level:
      div += 1
      level = 1
  return problem_urls
