#!/usr/bin/python3
"""
User view module for handling all default RESTful API actions
"""

from flask import jsonify, request, abort, make_response
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """
    Retrieves the list of all User objects: GET /api/v1/users
    """
    return jsonify([user.to_dict() for user in storage.all(User).values()])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """
    Retrieves a User object: GET /api/v1/users/<user_id>
    If the user_id is not linked to any User object, raise a 404 error
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """
    Deletes a User object: DELETE /api/v1/users/<user_id>
    If the user_id is not linked to any User object, raise a 404 error
    Returns an empty dictionary with the status code 200
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """
    Creates a User: POST /api/v1/users
    If the HTTP request body is not valid JSON,
    raise a 400 error with the message Not a JSON
    If the dictionary doesn’t contain the key email,
    raise a 400 error with the message Missing email
    If the dictionary doesn’t contain the key password,
    raise a 400 error with the message Missing password
    Returns the new User with the status code 201
    """
    if not request.json:
        abort(400, description="Not a JSON")
    if 'email' not in request.json:
        abort(400, description="Missing email")
    if 'password' not in request.json:
        abort(400, description="Missing password")

    data = request.get_json()
    new_user = User(**data)
    storage.new(new_user)
    storage.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """
    Updates a User object: PUT /api/v1/users/<user_id>
    If the user_id is not linked to any User object, raise a 404 error
    If the HTTP request body is not valid JSON,
    raise a 400 error with the message Not a JSON
    Update the User object with all key-value pairs of the dictionary
    Ignore keys: id, email, created_at and updated_at
    Returns the User object with the status code 200
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    if not request.json:
        abort(400, description="Not a JSON")

    data = request.get_json()
    ignored_keys = {'id', 'email', 'created_at', 'updated_at'}

    for key, value in data.items():
        if key not in ignored_keys:
            setattr(user, key, value)

    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
