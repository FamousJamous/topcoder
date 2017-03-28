import os

def gen_sh(path, lines):
  if os.path.isfile(path):
    return
  open(path, "w").write("\n".join(lines))
  os.chmod(path, 0x755)
