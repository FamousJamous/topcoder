#!/usr/bin/python
import datetime
import os
import re
from get_html_cached import get_html_cached

def get_match_list_html(data_dir, view, start):
  print "get_match_list_html view %d start %d" %(view, start)
  url = "https://www.topcoder.com/tc?module=MatchList&sc=&sd=&nr=%d&sr=%d" %(view, start)
  print "using url " + url
  today = datetime.datetime.now().date()
  file_name = "match_list.%d.%d.%d.%d.%d" %(view, start, today.year, today.month, today.day)
  return get_html_cached(url, data_dir, file_name)

def parse_match_list_html(match_list_html):
  srm_urls = {}
  for line in match_list_html:
    res = re.search(r'<a href="(\S+)">SRM (\S+)</a></td>', line)
    if not res:
      res = re.search(r'<a href="(\S+)">Member SRM (\S+)</a></td>', line)
      if not res:
        continue
    url = "https://community.topcoder.com/" + res.groups()[0]
    num = float(res.groups()[1])
    srm_urls[num] = url
  return srm_urls

def save_srm_urls(srm_urls, data_dir, first, last):
  save_file = open("%s/srm_urls.%s_%s" %(data_dir, first, last), "w")
  for num, url in srm_urls.iteritems():
    save_file.write("%s %s\n" %(num, url))

def get_srm_urls_file(srm_num, data_dir):
  for file_name in os.listdir(data_dir):
    res = re.match(r'srm_urls.(\S+)_(\S+)', file_name)
    if not res:
      continue
    first = float(res.groups()[0])
    last = float(res.groups()[1])
    if first <= srm_num and srm_num <= last:
      return open("%s/%s" %(data_dir, file_name))

def get_srm_url_from_file(srm_urls_file, srm_num):
  for line in srm_urls_file.readlines():
    [ num, url ] = line.strip().split(' ')
    if srm_num == float(num):
      return url

def get_srm_urls(srm_num, data_dir, view, start):
  match_list_html = get_match_list_html(data_dir, view, start)
  srm_urls = parse_match_list_html(match_list_html)
  return [ srm_urls, min(srm_urls), max(srm_urls) ]

def create_srm_urls_file(srm_num, data_dir):
  view = 50
  start = 1
  [ srm_urls, first, last ] = get_srm_urls(srm_num, data_dir, view, start)
  while srm_num < first or last < srm_num:
    if srm_num < first:
      start += last - srm_num + 50
    else:
      start -= last - srm_num + 50
    [ srm_urls, first, last ] = get_srm_urls(srm_num, data_dir, view, start)
  save_srm_urls(srm_urls, data_dir, first, last)
  return get_srm_urls_file(srm_num, data_dir)

def get_srm_url(srm_num, data_dir):
  srm_urls_file = get_srm_urls_file(srm_num, data_dir)
  if not srm_urls_file:
    srm_urls_file = create_srm_urls_file(srm_num, data_dir)
  return get_srm_url_from_file(srm_urls_file, srm_num)
