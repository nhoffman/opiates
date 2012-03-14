#!/bin/bash

# set -o verbose

confdir=/mnt/mass-spec/AA222_LCMS_Data/OpiateResearch/software_development/config

if [ ! -d $confdir ]; then
    echo "cannot see $confdir"
    exit 1
fi

# get config files from lilith share mounted to sci
cp $confdir/matrix.xlsx opiate/data
cp $confdir/qa.xlsx opiate/data

chown -R ${SUDO_USER-$USER} opiate/data
