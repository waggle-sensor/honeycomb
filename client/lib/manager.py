from enum import Enum
import logging
import os
import shutil

from job import job
# Create an enumeration for our states. This seems a bit more elegant than just using hard-coded strings. Might delete later if this complicates things
class State(Enum):
    IDLE = 1
    UPDATING = 2
    STOPPED = 3
    UNINITIALIZED = 4


# maintain a list of jobs, or pending updates
class hc_manager:

# maintaining a 'state' across the manager allows for transparency of operations in the bigger picture# 

    def __init__(self):
        self.__state = State.IDLE
        self.__jobs = []
        logging.basicConfig(level=logging.INFO)

    def getState(self):
        return self.__state

    def setState(self, newState):
        self.__state = newState


# add has an optional parameter to make the new job LIFO, instead of FIFO
    def addJob(self, manifest, job_dir, LIFO=False ): 
        
        # 

        if LIFO == True:
            self.__jobs.insert(0, job(manifest))
        else:
            self.__jobs.append(job(manifest, job_dir))

    def getJobs(self):
        return self.__jobs

    # take an index for the job we want to run. By default, we want a queue, so we run the 0th job.
    def runJob(self, index=0):

        job_to_run = self.getJobs().pop(index)
        logging.info(os.getcwd())

        # change into job dir
        
        os.chdir(f"./jobs/{job_to_run.get_job_dir()}/")

        job_to_run.state_check()
        job_to_run.install_upgrade()
        job_to_run.verify_upgrade()

        # now it's all said and done- delete the job dir and change back
        os.chdir("../../")
        shutil.rmtree(f"./jobs/{job_to_run.get_job_dir()}/")  



