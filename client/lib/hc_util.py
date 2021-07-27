import os 
import json
import logging
import tarfile
import hashlib

def init_upgrade_env(payload):
    logging.info("Creating upgrade environment")
    
    

    # look for upgrade file based on where the payload says it is
    if not os.path.isfile(f"./upgrades/{payload['config_file']}"):
        return { "message" : f"payload file ./upgrades/{payload['config_file']} not found",
                "return_code" : 400
                }

    # checking to see we have a .tar or .tar.gz
    if not payload["config_file"].endswith(".tar") and not payload["config_file"].endswith(".tar.gz"):
            
            return { "message" : f"payload file {payload['config_file']} is not a .tar or .tar.gz file",
                    "return_code" : 400
                }

    # upgrade env has already been created? 

    upgrade_name = f"{payload['peripheral_name']}-{payload['config_version']}"
    if os.path.isdir(f"./jobs/{upgrade_name}"):
        
        return { 
            "message" : f"job directory {upgrade_name} already exists",
            "return_code" : 400
        }

    
    config_file = tarfile.open(f"./upgrades/{payload['config_file']}", "r:*")
    os.mkdir(f"./jobs/{upgrade_name}")
    os.chdir(f"./jobs/{upgrade_name}")
    # Try to extract the tarfile
    try:
        config_file.extractall()
    except tarfile.ReadError: 
        return { 
            "message" : f"ReadError: Could not extract {payload['config_file']}",
            "return_code" : 400
        }

    config_file.close()

    # if all is good, return it as so
    return {
        "message" : "All good",
        "return_code" : 200
    }


def check_payload_validity(payload): 
    
    # check for a set of keys in our payload that we really need 
    fields = ["node_id", "flags", "peripheral_name", "config_version", "config_file" ]
    
    for field in fields:
        if field not in payload:
            return { 
                "message" : f"{field} was not found in payload",
                "return_code" : 400
            }

        logging.info("Payload request is valid")
    if os.path.exists("/etc/waggle/node-id"):
        with open("/etc/waggle/node-id") as nodeIDFile:
            nodeID = nodeIDFile.readline()
            if nodeID != payload["node_id"]:

                return { 
                    "message" : f"local nodeID {nodeID} does not match payload nodeID {payload['node_id']}",
                    "return_code" : 400
                }

    # If all is good, return ok
    return {
        "message" : "All good",
        "return_code" : 200
    }

def verify_checksum(payload):

    upgrade_name = f"{payload['peripheral_name']}-{payload['config_version']}"

    # open our md5sum.chk file and verify checksums
    # TODO: should I add a try/except here? 

    """ Our hashfile will have lines in the form of:
        MD5SUM  /path/to/file
        The two spaces between the sum and the path are why we go from index 0 to 2 on lines 103-104
    """ 
    with open("md5sum.chk", "r") as hashfile:

        for line in hashfile:

            # get the path and the hash
            current_hash = line.split(" ")[0]
            current_file = line.split(" ")[2].replace("\n", "")
            
            """ 
                because of the way that md5sum.chk is created, the hash will always differ
                when the file is being written. it checksums itself, but then adds more data after,
                making the checksum inaccurate.
                If this is a big deal, you might have to change how the checksums are generated in
                the ./upgrades/build_upgrade.sh file. I think it's fine, though
            """
            if current_file == "./md5sum.chk":
                continue

            # open each file in the checksum file and verify the checksum 

            with open(current_file, "rb") as tmpfile:
                
                hash = hashlib.md5()
                fcontent = tmpfile.read()
                hash.update(fcontent)
                file_hash = hash.hexdigest()

                if file_hash != current_hash:
                    
                    return {
                        "message" : f"{current_file} DOES NOT MATCH THE HASH",
                        "return_code" : 400
                    }


    # if all is good, return it as so
    return {
        "message" : "All good",
        "return_code" : 200
    }



