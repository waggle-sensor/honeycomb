# Honeycomb docs
## What is Honeycomb? 
* Honeycomb is a peripheral configuration versioning manager for Wild SAGE nodes. It will allow users to update and manage the state/configuration of their peripherals and the nodes they rest in.

## Why do we need this?
* When dealing with any fleet of nodes, doing the same systemic upgrade to a peripheral configuration often requires a developer to interface with the peripheral directly, which can be a massive drain of time or resources. Honeycomb will streamline the process of managing nodes, all the while keeping tabs of the overall node state for diagnostic analysis. 

-------
## Getting Started

Honeycomb imposes a set of guidelines pieces of update code to maximize modularity and retain insight into the process. The payload for your update must be in a .zip file. **It is assumed that these files will be in the root directory when the upgrade is unzipped, unless specified in `metadata.json`**

Required files: 
* `hc_state_check.sh`: check that your periperhal is not already in the target state. If it is, return 1. Otherwise, return with 0. 
* `hc_install_update.sh`: This is where your main driver code will rest. If the update runs successfully, return with 0. Otherwise, return with 1. 
* `hc_verify_update.sh`: Verify that your update took your peripheral into the goal state. If your check passes, return with 0. Otherwise, return with 1.
* `metadata.json`: Basic information regarding your update payload. A skeleton with required fields is provided.

**Note: `hc_state_check.sh`, `hc_install_update.sh`, and `hc_verify_update.sh` may return failure codes other than 1. Any error code greater than 1 is user-defined, so keep track of their meanings.**

## `metadata.json` structure
Your `metadata.json` tells the Honeycomb client-side everything it needs to know about your upgrade. It *must* have the following fields- failure to include them will prevent your upgrade job from running. A skeleton metadata.json is provided in **TODO: PROVIDE METADATA SKELETON LINK**. 

* `peripheral_name`: (String) The name of the peripheral being updated. Used for identification purposes. 
* `config_version`: (String) A config version number. If no `upgrade_name` field is provided, the generated upgrade name will be `peripheral_name`-`config_version`. 
* `retry_state_check`: (Int) How many times you want to retry the `hc_state_check.sh` script if it fails. 
    * 0: Do not retry
    * -1: Retry until it passes. Don't blame me if this loops forever!
* `retry_install`: (Int) How many times you want to retry the `hc_install_upgrade.sh` script if it fails. 
    * 0: Do not retry
    * -1: Retry until it passes. 
* `retry_verify`: (Int) How many times you want to retry the `hc_verify_install.sh` script if it fails. 
    * 0: Do not retry
    * -1: Retry until it passes. 
* `force_install`: (Bool) Do not run `hc_state_check.sh`.

### Optional fields:
* `description`: (String) A description of your upgrade. Not necessary for Honeycomb's workings, but it might be useful for the user. 
* `upgrade_name`: (String) The name of this upgrade. If not provided, a name is generated in the convention of `peripheral_name`-`config_version`. 
* `root_dir`: (String) Where Honeycomb will look for the `hc_dostuff` files. If this directory does not exist, the job will fail and not be added.  





