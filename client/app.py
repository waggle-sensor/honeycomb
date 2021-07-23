"""
honeycomb main manager
Written by Kenan- yell at him if this breaks
"""

import logging
import sys

# this might be a bad way to import libraries/blueprints, gotta fix this later
sys.path.append("./routes/")
sys.path.append("./lib")

from flask import Flask
from flask_restful import Resource, Api

from upgrade_peripheral import upgrade
# from job import job
from manager import hc_manager



# All output for this service will be piped to journalctl under the honeycomb service
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
api = Api(app)
app.register_blueprint(upgrade)

# use app as a context
honeycomb = hc_manager()
app.honeycomb = honeycomb

@app.route("/")
def hello_world():
    
    return { "message" : f"Honeycomb is currently {app.honeycomb.getState()}" }


if __name__ == "__main__":
    app.run(debug=True)

