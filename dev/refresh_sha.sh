#!/bin/bash

set -o verbose

shafile=opiate/data/sha
cat ${shafile:?}
rm -f ${shafile:?}
git checkout ${shafile:?}
cat ${shafile:?}
git --no-pager log -1
