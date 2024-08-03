#!/usr/bin/python3
"""
Index module for API endpoints
Defines routes for status and object counts
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
    """
    Route to check the status of the API
    Returns a JSON response with status 'OK'
    """
    data = {
        "status": "OK"
    }

    resp = jsonify(data)
    resp.status_code = 200

    return resp


@app_views.route("/stats", methods=['GET'], strict_slashes=False)
def stats():
    """
    Route to retrieve the number of each object type
    Returns a JSON response with the count of each object type
    """
    data = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User"),
    }

    resp = jsonify(data)
    resp.status_code = 200

    return resp
