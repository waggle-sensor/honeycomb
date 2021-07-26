#!/bin/bash

if [ "$1" = "" ]; then
    echo "No upgrade directory specified, exiting"
    exit 1
fi

# go to the directory
cd "$1"

# grab the upgrade name, or generate it
upgrade_name="$(cat metadata.json | jq .upgrade_name | tr -d '"')"

if [ "$upgrade_name" = "null" ];
then 
    upgrade_name="$(cat metadata.json  | jq .peripheral_name | tr -d '"')-$(cat metadata.json  | jq .config_version | tr -d '"')"
fi

echo "Making upgrade .tar.gz for $upgrade_name"

# generate our checksum file
find . -type f -exec md5sum {} \; > md5sum.chk

tar cfvz "../$upgrade_name.tar.gz" *
