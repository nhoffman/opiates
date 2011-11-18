#!/bin/bash

set -o verbose

confdir=/home/LABMED/nhoffman/mnt/lilith/uwmc_chemistry/NewOpiatesAug2010/software_development/config

# get config files from lilith share mounted to sci
scp sci:$confdir/matrix.xlsx opiate/data
scp sci:$confdir/qa.xlsx opiate/data
