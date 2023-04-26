#!/usr/bin/python3
"""
Script that  starts Flask app
Listens on 0.0.0.0 port 5000
"""
from flask import Flask, render_template
from models import storage
from models.state import State
import models


app = Flask(__name__)


@app.teardown_appcontext
def teardown_session(self):
    """tear down the sqlalchemy session """
    storage.close()


@app.route('/states_list', strict_slashes=False)
def states_list():
    """displays all states"""
    states = models.storage.all(State)
    list_of_states = [state for state in states.values()]
    return render_template("7-states_list.html",
                           list_of_states=list_of_states)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
