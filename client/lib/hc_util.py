import os
import json
import logging
from sys import path
import tarfile
import hashlib
import shutil


def check_manifest_validity(manifest, upgrade_name):

    required_fields = [
        "config_version",
        "retry_state_check",
        "retry_install",
        "retry_verify",
        "peripheral_name",
        "force_install",
    ]

    for field in required_fields:
        if field not in manifest:
            return {
                "message": f"{field} was not found in manifest for upgrade {upgrade_name}- aborting",
                "return_code": 400,
            }

    logging.info(f"Upgrade metadata.json all good ✓")
    return {"message": "All good\n", "return_code": 200}


def check_required_files(manifest, job_path):

    required_files = [
        "hc_state_check.sh",
        "hc_install_upgrade.sh",
        "hc_verify_upgrade.sh",
    ]

    # for each required file, check if it's in our root dir
    all_files = os.listdir(job_path)
    for file in required_files:
        if not os.path.isfile(f"{job_path}/{file}"):
            logging.info(f"ERROR: Job is missing file {file} in path {job_path}")
            return {
                "message": f"Could not find file {job_path}/{file}",
                "return_code": 400,
            }
    return {"message": "All good\n", "return_code": 200}


def check_for_tarfile(fname):

    fullname = f"./upgrades/{fname}.tar.gz"

    if not os.path.isfile(fullname):
        return {"message": f"Could not find file {fullname}", "return_code": 400}
    else:
        return {"message": f"File {fullname}", "return_code": 200}


def init_upgrade_env_tar(fname):
    logging.info("Creating upgrade environment")

    # look for upgrade file based on where the payload says it is
    # if not os.path.isfile(f"./upgrades/{payload['config_file']}"):
    #     return {
    #         "message": f"payload file ./upgrades/{payload['config_file']} not found\n",
    #         "return_code": 400,
    #     }

    # upgrade env has already been created?
    if os.path.isdir(f"./jobs/{fname}"):

        return {
            "message": f"job directory {fname} already exists\n",
            "return_code": 400,
        }

    config_file = tarfile.open(f"./upgrades/{fname}.tar.gz", "r:*")
    os.mkdir(f"./jobs/{fname}")
    # Try to extract the tarfile
    try:
        config_file.extractall(path=f"./jobs/{fname}")
    except tarfile.ReadError:
        return {
            "message": f"ReadError: Could not extract {fname}.tar.gz\n",
            "return_code": 400,
        }

    config_file.close()

    # if all is good, return it as so
    return {"message": "All good\n", "return_code": 200}


def verify_checksum_tar(fname):

    # open our md5sum.chk file and verify checksums
    # TODO: should I add a try/except here?

    """Our hashfile will have lines in the form of:
    MD5SUM  /path/to/file
    The two spaces between the sum and the path are why we go from index 0 to 2 on lines 103-104
    """
    with open(f"./jobs/{fname}/md5sum.chk", "r") as hashfile:

        for line in hashfile:

            # get the path and the hash
            current_hash = line.split(" ")[0]
            current_file = line.split(" ")[2].replace("\n", "")
            current_file = f"./jobs/{fname}/{current_file.replace('./', '')}"

            """ 
                because of the way that md5sum.chk is created, the hash will always differ
                when the file is being written. it checksums itself, but then adds more data after,
                making the checksum inaccurate.
                If this is a big deal, you might have to change how the checksums are generated in
                the ./upgrades/build_upgrade.sh file. I think it's fine, though
            """
            if current_file == f"./jobs/{fname}/md5sum.chk":
                continue

            # open each file in the checksum file and verify the checksum

            with open(current_file, "rb") as tmpfile:

                hash = hashlib.md5()
                fcontent = tmpfile.read()
                hash.update(fcontent)
                file_hash = hash.hexdigest()

                if file_hash != current_hash:

                    # clean up our environment
                    shutil.rmtree(f"./jobs/{fname}")
                    return {
                        "message": f"{current_file} DOES NOT MATCH THE HASH\n",
                        "return_code": 400,
                    }

    return {"message": "All good\n", "return_code": 200}
