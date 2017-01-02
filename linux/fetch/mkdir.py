import os

def mkdir(name):
  if os.path.isdir(name):
    return
  os.mkdir(name)

