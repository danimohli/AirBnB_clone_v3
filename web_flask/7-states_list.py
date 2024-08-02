#!/usr/bin/python3
"""
Flask web application that fetches data from storage engine
and displays a list of all State objects in DBStorage.
"""

from flask import Flask, render_template, jsonify
from models import storage
from models.state import State
import logging


app = Flask(__name__)

logging.basicConfig(level=logging.INFO)


@app.route('/states_list', strict_slashes=False)
def states_list():
    """
    Displays a HTML page with the list of all State objects sorted by name.
    """
    try:
        states = storage.all(State).values()
        sorted_states = sorted(states, key=lambda state: state.name)
        return render_template('7-states_list.html', states=sorted_states)
    except Exception as e:
        logging.error(f"Error fetching states: {e}")
        return jsonify({'error': 'Unable to fetch states'}), 500


@app.teardown_appcontext
def teardown_db(exception):
    """
    Closes the storage session after each request.
    """
    storage.close()
    if exception:
        logging.error(f"Teardown error: {exception}")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
