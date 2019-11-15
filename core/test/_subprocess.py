# -*- coding: utf-8 -*-
# Created by #chuyong, on 2019/10/28.
# Copyright (c) 2019 3KWan.
# Description :
import os
import subprocess
import sys
from importlib import reload

# reload(sys)

if __name__ == '__main__':

    child = subprocess.Popen(["dir", ], shell=True, cwd=os.path.dirname(os.path.abspath(__file__)), encoding="utf-8")
    child.wait()
    print("---->", child.returncode)
    print(type(child))
    print(dir(child))

