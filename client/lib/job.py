import logging
import sys
import os
import subprocess


sys.path.append("./lib")


class job:
    def __init__(self, manifest, job_dir):
        logging.basicConfig(level=logging.INFO)
        # go through every required field in the manifest and check for it
        # manifest refers to the manifest.json file that is required in every upgrade zip

        self.__job_dir = job_dir
        """ important distinction that may be confusing- the job_dir is separate from
            the upgrade name. The job_dir refers to which folder hc can access this upgrade from. 
            The upgrade_name is more of a label, and identifies the upgrade to the user.
            It might be worth changing these to be clearer in the future.
        """
        self

        if "upgrade_name" in manifest:
            self.__name = manifest["upgrade_name"]
        else:
            self.__name = f"{manifest['peripheral_name']}-{manifest['config_version']}"

        # run our checks
        logging.info(f"Checking validity of {self.__name} upgrade payload")

        logging.info(f"Checking existence of required files in {self.__name} root dir")

        self.set_retry_values(manifest)

    def get_name(self):
        return self.__name

    def set_retry_values(self, manifest):

        self.__state_check_retry = manifest["retry_state_check"] + 1
        self.__install_retry = manifest["retry_install"] + 1
        self.__verify_retry = manifest["retry_verify"] + 1

    def get_retry_values(self, manifest):
        return {
            "state_check": self.__state_check_retry,
            "install": self.__install_retry,
            "verify": self.__verify_retry,
        }

    # can I do this job? (not talking to myself)
    # def is_job_enabled():
    # def is_job_disabled():

    def get_job_dir(self):
        return f"./jobs/{self.__job_dir}/"

    # TODO: if the three core hc files have -1 as their retry vals, loop it forever till it passes

    def state_check(self):

        # we need to be in the root directory to make sure this process runs smoothly

        # Run our state check as many times as we need
        for x in range(0, self.__state_check_retry):
            logging.info(
                f"Running {self.__name} state check, try {x+1} of {self.__state_check_retry}"
            )

            z = subprocess.run(
                "./hc_state_check.sh",
                subprocess.STDOUT,
                cwd=self.get_job_dir(),
                shell=True,
            )
            if z.returncode != 0:
                logging.info(f"State check FAILED with error code {z.returncode}")
            else:
                logging.info(f"State check PASSED, proceeding to install")
                return True
                break

        return False

    def install_upgrade(self):

        # Run our install as many times as we need
        for x in range(0, self.__install_retry):
            logging.info(
                f"Running {self.__name} upgrade install, try {x+1} of {self.__state_check_retry}"
            )

            z = subprocess.run(
                "./hc_install_upgrade.sh",
                subprocess.STDOUT,
                cwd=self.get_job_dir(),
                shell=True,
            )
            if z.returncode != 0:
                logging.info(f"Install FAILED with error code {z.returncode}")
            else:
                logging.info(f"Install PASSED, proceeding to verification")
                return True
                break

        return False

    def verify_upgrade(self):

        for x in range(0, self.__verify_retry):
            logging.info(
                f"Running {self.__name} upgrade verification, try {x+1} of {self.__state_check_retry}"
            )

            z = subprocess.run(
                "./hc_verify_upgrade.sh",
                subprocess.STDOUT,
                cwd=self.get_job_dir(),
                shell=True,
            )
            if z.returncode != 0:
                logging.info(f"Verification FAILED with error code {z.returncode}")
            else:
                logging.info(
                    f"Verification PASSED, upgrade complete! Proceeding to cleanup."
                )
                return True
                break

        return False


# TODO: Remove force_install option from hc metadata.json and README
