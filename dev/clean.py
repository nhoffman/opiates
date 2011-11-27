#!/usr/bin/env python

import fileinput
from os import path
import sys

for line in fileinput.input([path.join('opiate','__init__.py')], inplace = True):
    if line.startswith('_sha ='):
        line = "_sha = ''\n"
    sys.stdout.write(line)



