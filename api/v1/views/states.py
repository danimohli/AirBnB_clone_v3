#!/usr/bin/python3
"""
State view module for handling all default RESTful API actions
"""

from flask import jsonify, request, abort, make_response
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """
    Retrieves the list of all State objects: GET /api/v1/states
    """
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """
    Retrieves a State object: GET /api/v1/states/<state_id>
    If the state_id is not linked to any State object, raise a 404 error
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """
    Deletes a State object: DELETE /api/v1/states/<state_id>
    If the state_id is not linked to any State object, raise a 404 error
    Returns an empty dictionary with the status code 200
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """
    Creates a State: POST /api/v1/states
    If the HTTP body request is not valid JSON,
    raise a 400 error with the message Not a JSON
    If the dictionary doesn’t contain the key name,
    raise a 400 error with the message Missing name
    Returns the new State with the status code 201
    """
    if not request.json:
        abort(400, description="Not a JSON")
    if 'name' not in request.json:
        abort(400, description="Missing name")

    data = request.get_json()
    new_state = State(**data)
    storage.new(new_state)
    storage.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """
    Updates a State object: PUT /api/v1/states/<state_id>
    If the state_id is not linked to any State object,
    raise a 404 error
    If the HTTP body request is not valid JSON,
    raise a 400 error with the message Not a JSON
    Update the State object with all key-value pairs of the dictionary
    Ignore keys: id, created_at, updated_at
    Returns the State object with the status code 200
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    if not request.json:
        abort(400, description="Not a JSON")

    data = request.get_json()
    ignored_keys = {'id', 'created_at', 'updated_at'}

    for key, value in data.items():
        if key not in ignored_keys:
            setattr(state, key, value)

    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
