#!/usr/bin/python3
"""
City view module for handling all default RESTful API actions
"""

from flask import jsonify, request, abort, make_response
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """
    Retrieves the list of all City objects of a State:
    GET /api/v1/states/<state_id>/cities
    If the state_id is not linked to any State object,
    raise a 404 error
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """
    Retrieves a City object: GET /api/v1/cities/<city_id>
    If the city_id is not linked to any City object,
    raise a 404 error
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """
    Deletes a City object: DELETE /api/v1/cities/<city_id>
    If the city_id is not linked to any City object, raise a 404 error
    Returns an empty dictionary with the status code 200
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """
    Creates a City: POST /api/v1/states/<state_id>/cities
    If the state_id is not linked to any State object, raise a 404 error
    If the HTTP body request is not valid JSON,
    raise a 400 error with the message Not a JSON
    If the dictionary doesn’t contain the key name,
    raise a 400 error with the message Missing name
    Returns the new City with the status code 201
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")
    if 'name' not in request.json:
        abort(400, description="Missing name")

    data = request.get_json()
    new_city = City(state_id=state_id, **data)
    storage.new(new_city)
    storage.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """
    Updates a City object: PUT /api/v1/cities/<city_id>
    If the city_id is not linked to any City object, raise a 404 error
    If the HTTP request body is not valid JSON,
    raise a 400 error with the message Not a JSON
    Update the City object with all key-value pairs of the dictionary
    Ignore keys: id, state_id, created_at and updated_at
    Returns the City object with the status code 200
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if not request.json:
        abort(400, description="Not a JSON")

    data = request.get_json()
    ignored_keys = {'id', 'state_id', 'created_at', 'updated_at'}

    for key, value in data.items():
        if key not in ignored_keys:
            setattr(city, key, value)

    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
