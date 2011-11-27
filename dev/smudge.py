#!/usr/bin/env python

import subprocess
import fileinput
from os import path
import sys

sha = subprocess.check_output(
    args = ['git', '--no-pager', 'log', '--pretty=format:"%h"', '-1']
    ).strip('"')

for line in fileinput.input([path.join('opiate','__init__.py')], inplace = True):
    if line.startswith('_sha ='):
        line = "_sha = '.%s'\n" % sha
    sys.stdout.write(line)
