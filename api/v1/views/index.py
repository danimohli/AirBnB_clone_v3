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

classes = {"users": "User", "places": "Place", "states": "State",
           "cities": "City", "amenities": "Amenity",
           "reviews": "Review"}


@app_views.route('/status', methods=['GET'])
def status():
    """
    Route to check the status of the API
    Returns a JSON response with status 'OK'
    """
    return jsonify({'status': 'OK'})


@app_views.route('/stats', methods=['GET'])
def count():
    """
    Route to retrieve the number of each object type
    Returns a JSON response with the count of each object type
    """
    count_dict = {}
    for cls in classes:
        count_dict[cls] = storage.count(classes[cls])
    return jsonify(count_dict)
