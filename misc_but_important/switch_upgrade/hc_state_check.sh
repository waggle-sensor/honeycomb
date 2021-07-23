#!/bin/bash

<< headercomment 
we need to get the current config from the switch. We only care about the header, which looks like:

!Current Configuration:
!
!System Description "EdgeSwitch 8 150W, 1.9.2, Linux 3.6.5-03329b4a, 1.1.0.5102011"
!System Software Version "1.9.2"
!System Up Time          "22 days 2 hrs 6 mins 43 secs"
!Additional Packages     QOS,IPv6 Management,Routing
!Current SNTP Synchronized Time: SNTP Last Attempt Status Is Not Successful
! waggle config version: x.x
!

headercomment

# before any of this happens, we need the actual config file in some form

# checking whether our current config is ahead of the upgrade config

upgrade_version=$(cat metadata.json | jq .config_version | tr -d '"')
current_version="$(cat mock_config | grep waggle | cut -d':' -f2)"

pf="Edgeswitch upgrade"

echo "Beginning state check for $pf for upgrade $current_version -> $upgrade_version"

if ! dpkg --compare-versions "$current_version" "lt" "$upgrade_version"; then
    echo "$pf: State check FAILED (exiting with 1)"
    exit 1
else
    echo "$pf: State check PASSED (exiting with 0)"
    exit 0
    # if we're adding more checks after this, delete the exit line
fi

