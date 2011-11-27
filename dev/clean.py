#!/usr/bin/env python

import fileinput
from os import path

for line in fileinput.input([path.join('opiate','__init__.py')], inplace = True, backup = '.bak'):
    if line.startswith('_sha ='):
        line = "_sha = ''"
    print line



