#!/bin/bash

new_version="1.2.4" 

if echo $new_version > /etc/waggle/honeycomb/version ; then
    echo "Successfully upgraded to $new_version"
    exit 0
else
    echo "Could not upgrade to $new_version"
    exit 1
fi

