from flask import Blueprint, render_template, session, abort, request
from flask import current_app as app

from hc_util import (
    check_required_files,
    check_manifest_validity,
    check_for_tarfile,
    init_upgrade_env_tar,
    verify_checksum_tar,
)

import os
import json
import logging

logging.basicConfig(level=logging.INFO)

upgrade = Blueprint("upgrade", __name__)


@upgrade.route("/queue-upgrade", methods=["POST", "GET"])
def process():

    # get the query args
    # we need file_name
    if request.args.get("filename") is None:
        return "No filename query arg provided!", 400

    fname = request.args.get("filename")

    # go through every check we have, if it errors out, return that message and code

    is_tarfile = check_for_tarfile(fname)
    if is_tarfile["return_code"] != 200:
        return is_tarfile["message"], is_tarfile["return_code"]

    env_validity = init_upgrade_env_tar(fname)
    if env_validity["return_code"] != 200:
        return env_validity["message"], env_validity["return_code"]

    checksum_validity = verify_checksum_tar(fname)
    if checksum_validity["return_code"] != 200:
        return checksum_validity["message"], checksum_validity["return_code"]

    with open(f"./jobs/{fname}/metadata.json") as manifest:
        manifest_json = json.load(manifest)

    # TODO: check error codes here
    are_files_present = check_required_files(manifest_json, f"./jobs/{fname}")
    if are_files_present["return_code"] != 200:
        return are_files_present["message"], are_files_present["return_code"]

    valid_manifest = check_manifest_validity(manifest_json, fname)
    if valid_manifest["return_code"] != 200:
        return valid_manifest["message"], valid_manifest["return_code"]

    app.honeycomb.addJob(manifest_json, fname)

    # TODO: Change this success message
    return {"message": "Job has been added to queue\n"}, 200
