#!/usr/bin/python
import os
import urllib2

def get_html_cached(url, file_name):
  path = "data/" + file_name
  if not os.path.isfile(path):
    html = open(path, "w")
    html.write(urllib2.urlopen(url).read())
  return open(path)
