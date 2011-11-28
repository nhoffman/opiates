#!/bin/bash

cat opiate/_sha.py
rm -f opiate/_sha.py
git checkout opiate/_sha.py
cat opiate/_sha.py
git --no-pager log -1
