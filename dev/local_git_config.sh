#!/bin/bash

cp .git/config git-config.bak
git config --remove-section filter.sha
cat dev/config_sha >> .git/config
