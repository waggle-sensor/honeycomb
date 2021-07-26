from flask import Blueprint, render_template, session, abort, request
from flask import current_app as app

from hc_util import init_upgrade_env, verify_checksum, check_payload_validity

import os
import json
import logging
import tarfile

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

   
   # verify the checksum
    checksum_validity = verify_checksum(payload)
    if checksum_validity["return_code"] >= 400:
        return checksum_validity["message"], checksum_validity["return_code"]

    
    return { "message" : "Upgrade called successfully" }, 200

# TODO: It might be useful to move these computational functions out of this route? maybe import them from somewhere.  
# TODO: make a cleanup function if the payload is not good. basically just delete the upgrade folder

