#!/usr/bin/env python

import compileall
import os, sys

path = os.path.abspath(os.path.dirname(sys.argv[0]))

print "Compiling files..."

compileall.compile_dir(path+str("/src"), force=1)
compileall.compile_dir(path+str("/src/model"), force=1)
compileall.compile_dir(path+str("/src/view"), force=1)

