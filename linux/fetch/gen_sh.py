import os

def gen_sh(path, lines):
  open(path, "w").write("\n".join(lines))
  os.chmod(path, 0x755)
