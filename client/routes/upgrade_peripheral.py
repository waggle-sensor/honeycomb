from flask import Blueprint, render_template, session, abort, request
from flask import current_app as app
import os 
import json
import logging

logging.basicConfig(level=logging.INFO)

upgrade = Blueprint("upgrade", __name__)

@upgrade.route("/upgrade", methods=['POST'])
def process():



    payload = request.json
    logging.info(payload)
    
    # go through every check we have, if it errors out, return that message and code
    # I don't think I can return a message or code directly from these check functions, 
    # So I have to check manually

    # check that we have a valid payload
    payload_validity = check_payload_validity(payload)
    if payload_validity["return_code"] >= 400:
        return payload_validity["message"], payload_validity["return_code"]
    
    # set up payload env
    env_validity = init_upgrade_env(payload)
    if env_validity["return_code"] >= 400:
        return env_validity["message"], env_validity["return_code"]

   
   # download the payload
    download_validity = retrieve_payload_contents(payload)
    if download_validity["return_code"] >= 400:
        return download_validity["message"], download_validity["return_code"]
    # add this change
    
    return { "message" : "Upgrade called successfully" }, 200

# TODO: It might be useful to move these computational functions out of this route? maybe import them from somewhere.  
# TODO: make a cleanup function if the payload is not good. basically just delete the upgrade folder

def init_upgrade_env(payload):
    logging.info("Creating upgrade environment")
    
    # upgrade name
    upgrade_name = f"{payload['peripheral_name']}-{payload['config_version']}"
    if os.path.isdir(f"./jobs/{upgrade_name}"):
        return { 
            "message" : f"job directory {upgrade_name} already exists",
            "return_code" : 400
        }

    os.chdir("./jobs/")
    os.mkdir(upgrade_name)

    return {
        "message" : "All good",
        "return_code" : 200
    }

def retrieve_payload_contents(payload): 

    # use 'config_link' to download the payload 
    # for now, since I don't want to host a local server, I'll have the zip downloaded
    logging.info("TODO: Implement payload download") 

    return {
        "message" : "All good",
        "return_code" : 200
    }

def check_payload_validity(payload): 
    
    # check for a set of keys in our payload that we really need 
    fields = ["node_id", "flags", "peripheral_name", "config_version", "config_link" ]
    
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