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
        self.check_manifest_validity(manifest)
        
        logging.info(f"Checking existence of required files in {self.__name} root dir")

        self.check_required_files(manifest) 

        self.set_retry_values(manifest)

    def check_manifest_validity(self, manifest):
        # add check for necessary hc files, make sure to chdir into the root_dir path (if provided)
        required_fields = ["config_version", "force_install","retry_state_check", "retry_install", "retry_verify", "peripheral_name", "force_install"]
        
        for field in required_fields:
            if field not in manifest:
               raise ValueError(f"{field} was not found in manifest for upgrade {self.__name}- aborting")

        logging.info(f"Upgrade {self.__name} metadata.json all good ✓")

    def check_required_files(self, manifest):
        
        job_path = f"./jobs/{self.__job_dir}/"

        required_files = ["hc_state_check.sh", "hc_install_upgrade.sh", "hc_verify_upgrade.sh"]

        # for each required file, check if it's in our root dir
        all_files = os.listdir(job_path)
        for file in required_files: 
            if not os.path.isfile(f"{job_path}{file}"):
                logging.info(f"ERROR: Job {self.__name} is missing file {file} in path {job_path}")

    def get_name(self):
        return self.__name

    def set_retry_values(self, manifest):

        self.__state_check_retry = manifest["retry_state_check"]
        self.__install_retry = manifest["retry_install"]
        self.__verify_retry = manifest["retry_verify"]
        self.__force_install = manifest["force_install"]


    def get_retry_values(self, manifest):
        return {
            "state_check" : self.__state_check_retry,
            "install" : self.__install_retry,
            "verify" : self.__verify_retry,
            "force_install" : self.__force_install
        }
        

    # can I do this job? (not talking to myself)
    # def is_job_enabled():
    # def is_job_disabled(): 

    def state_check(self):
        logging.info(f"Running {self.__name} State check")

        # we need to be in the root directory to make sure this process runs smoothly
        os.chdir(f"./jobs/{self.__job_dir}/")
        logging.info(f"Running {self.__name} STATE check")
        logging.info(os.getcwd())
        # for try in range(0, self.__state_check_retry):

        # TODO: this code keeps freezing for some reason
        
        z = subprocess.run("ls -la")
        logging.info(str(z.stdout))




