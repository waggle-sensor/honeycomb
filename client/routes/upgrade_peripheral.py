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
    # logging.info(payload)
    
    # go through every check we have, if it errors out, return that message and code


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

    # at this point, we're in the ./job/jobX directory, so we need to cd back to /honeycomb
    os.chdir("../../")

    # grab our metadata JSON, pass it to the job
    upgrade_name = f"{payload['peripheral_name']}-{payload['config_version']}"

    with open(f"./jobs/{upgrade_name}/metadata.json") as manifest:
        manifest_json = json.load(manifest)
        app.honeycomb.addJob(manifest_json, upgrade_name)
        logging.info("Job has been added to queue")
        logging.info(app.honeycomb.getJobs())

    # TODO: Change this success message
    return { "message" : "Upgrade called successfully" }, 200

# TODO: make a cleanup function if the payload is not good. basically just delete the upgrade folder

