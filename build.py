import os, subprocess, sys

HERE   = os.path.dirname(os.path.abspath(__file__))   # ...\example\PyForge
PARENT = os.path.dirname(HERE)                        # ...\example

sys.exit(subprocess.call(
    [sys.executable, os.path.join(HERE, "setup.py"),
     "build_ext", "--inplace", "--force"],
    cwd=PARENT,
))