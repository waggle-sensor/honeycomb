#!/bin/bash


# get the version from the file
version="$(cat /etc/waggle/honeycomb/version)"

if [ "$version" = "1.2.4" ]; then
    echo "Verified!, upgradied to $version"
    exit 0
else
    echo "install failed, exiting"
    exit 1
fi


