#!/usr/bin/sh

changesFile=changes
configFile=config.json

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

for dirname in ./tests/input/*; do

    python exo.py "$dirname/$configFile" "$dirname/$changesFile"
    diff result.json "tests/output/$(basename $dirname)/result.json"

    if [ $? -eq 1 ]; then
        echo -e ${RED}[Test fail]${NC}: $(basename $dirname)
    else
        rm -f result.json
        echo -e ${GREEN}[Test ok]${NC}: $(basename $dirname)
    fi

done
