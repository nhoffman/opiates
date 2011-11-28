#!/bin/bash

cp .git/config git-config.bak
(grep -v sha git-config.bak && cat dev/config_sha) > .git/config
