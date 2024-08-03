#!/usr/bin/python3
"""
app module for An API
"""

from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

app = Flask(__name__)

"""
Enable Cross-Origin Resource Sharing (CORS) for the API
"""
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})

"""
Disable strict slashes in URL routing
"""
app.url_map.strict_slashes = False

"""
Register the blueprint for the API views
"""
app.register_blueprint(app_views)


@app.teardown_appcontext
def tear(self):
    """
    Method called when the app context tears down.
    It ensures the storage engine is properly closed.
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """
    Handles 404 errors and returns a JSON formatted response.

    Args:
        error: The error that occurred.

    Returns:
        A JSON response with a 404 status code and
        an error message.
    """
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    """
    Set the host and port for the Flask app
    """
    HBNB_API_HOST = getenv("HBNB_API_HOST", '0.0.0.0')
    HBNB_API_PORT = int(getenv("HBNB_API_PORT", 5000))

    """
    Run the Flask app
    """
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
