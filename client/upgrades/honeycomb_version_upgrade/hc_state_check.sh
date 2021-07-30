#!/bin/bash


# check for our /etc/waggle/honeycomb/version file
new_version="1.2.4"

version=/etc/waggle/honeycomb/version

if ! [ -f "/etc/waggle/honeycomb/version" ]; then
    echo "/etc/waggle/honeycomb/version not found"
    exit 1
fi

# get the version from the file
old_version="$(cat /etc/waggle/honeycomb/version)"

if dpkg --compare-versions "$new_version" gt "$old_version" ; then
    echo "State check passed, upgrading from $old_version to $new_version"
    exit 0
else
    echo "State check failed, exiting"
    exit 1
fi


