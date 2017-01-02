from gen_sh import gen_sh

def gen_url(path, url):
  gen_sh(path + "/url.sh", [
    "#!/bin/bash",
    "echo \"" + url + "\"",
    "firefox --new-tab \"" + url + "\"&",
  ])
