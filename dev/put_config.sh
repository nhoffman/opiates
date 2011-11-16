#!/bin/bash

set -o verbose

confdir=/home/LABMED/nhoffman/mnt/lilith/uwmc_chemistry/NewOpiatesAug2010/software_development/config

# push config files to lilith share mounted to sci
scp opiate/data/*.xlsx sci:$confdir
