#!/usr/bin/python
import re
from get_html_cached import get_html_cached

SUB_QUOTE = re.compile("&quot;")
SUB_TAB = re.compile("<td ?[a-zA-Z0-9=\" ]*>")
SUB_CLEAR = re.compile("</[a-z0-9]*>|&#[0-9]*;|<b>|<td>|<table>|<pre>")
SUB_NEWLINE = re.compile("<[a-z0-9]* ?[a-zA-Z0-9=\" ]*>")

def format_problem(url, srm_num, div, level):
  cached_file_name = "srm%d.d%d.l%d" %(srm_num, div, level)
  formatted_file_name = "data/" + cached_file_name + ".formatted"
  formatted_file = open(formatted_file_name, "w")
  for line in get_html_cached(url, cached_file_name):
    line = SUB_QUOTE.sub("\"", line)
    line = SUB_TAB.sub("\t", line)
    line = SUB_CLEAR.sub("", line)
    line = SUB_NEWLINE.sub("\n", line)
    formatted_file.write(line)
    if "All rights reserved." in line:
      return formatted_file_name

def format_problems(srm_num, problem_urls):
  file_names = []
  for div, urls in problem_urls.iteritems():
    print "div %d" %(div)
    for level, url in urls.iteritems():
      print "level %d %s" %(level, url)
      if not url:
        continue
      file_names.append(format_problem(url, srm_num, div, level))
  return file_names
