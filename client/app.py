"""
honeycomb main manager
Written by Kenan- yell at him if this breaks
"""
import threading
import logging
import sys
import time

# this might be a bad way to import libraries/blueprints, gotta fix this later
sys.path.append("./routes/")
sys.path.append("./lib")

from flask import Flask
from flask_restful import Resource, Api

from upgrade_peripheral import upgrade
from job import job
from manager import hc_manager



# All output for this service will be piped to journalctl under the honeycomb service
logging.basicConfig(level=logging.INFO)


app = Flask(__name__)
api = Api(app)
app.register_blueprint(upgrade)

# use app as a context
honeycomb = hc_manager()
app.honeycomb = honeycomb

""" Set a timeout to check the honeycomb queue every x seconds, and run jobs
    To me, this is an ok way to accomplish the 'queue' functionality of honeycomb
    But I can see how this is janky, too- so this polling and execution part might
    need a refactor when scaled up. 
    The alternative is having /upgrade simply run the job as soon as it gets it. 
    BUT- there might be race conditions. that's what I'm getting hung up on.  
"""

def check_for_jobs():
    while True:
        
        jobList = app.honeycomb.getJobs()

        if len(jobList) > 0 :
            logging.info(f"Executing Job: {jobList[0].get_name()}")
            app.honeycomb.runJob()
        time.sleep(1)
    


check_thread = threading.Thread(target=check_for_jobs)
check_thread.start()

@app.route("/")
def hello_world():
    logging.info(app.honeycomb.getJobs())
    return { "message" : f"Honeycomb is currently {app.honeycomb.getState()}" }


if __name__ == "__main__":
    app.run(debug=True)

