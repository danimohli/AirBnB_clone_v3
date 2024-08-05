#!/usr/bin/python3
"""
This module handles all default RESTFul API actions for Place objects.
"""
from api.v1.views import (app_views, Place, City, User, storage)
from flask import (abort, jsonify, make_response, request)
import os


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def view_places_in_city(city_id):
    """
    Returns a list of all places in a city
    Retrieves all places within a city
    A list of dictionaries of place object
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    result = [place.to_dict() for place in city.places]
    return jsonify(result)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def view_place(place_id):
    """
    Returns a single place
    One place with the given id
    A single place object
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """
    Deleting one place
    Deletes a place based on the place_id of the JSON
    An empty dictionary
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """
    Creates a single place
    Create single place based on the JS
    A single place object created
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if not request.is_json:
        return jsonify(error="Not a JSON"), 400

    data = request.get_json()

    if 'user_id' not in data:
        return jsonify(error="Missing user_id"), 400
    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)
    if 'name' not in data:
        return jsonify(error="Missing name"), 400

    data['city_id'] = city_id
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """
    Updates a single place
    Place based on the JSON body
    Single place object updated
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if not request.is_json:
        return jsonify(error="Not a JSON"), 400

    data = request.get_json()

    ignore_keys = {'id', 'user_id', 'city_id', 'created_at', 'updated_at'}
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)

    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def list_places():
    """
    List all places of a JSON body
    All places of a JSON body
    Objects matching the search criteria
    """
    if not request.is_json:
        return jsonify(error="Not a JSON"), 400

    data = request.get_json()

    places = storage.all(Place).values()

    if 'states' in data:
        states = [storage.get("State", state_id) for state_id in data['states']]
        cities = [city for state in states for city in state.cities] if states else []
        places = [place for place in places if place.city_id in [city.id for city in cities]]

    if 'cities' in data:
        cities = [storage.get(City, city_id) for city_id in data['cities']]
        places = [place for place in places if place.city_id in [city.id for city in cities]]

    if 'amenities' in data:
        amenities = data['amenities']
        places = [place for place in places if all(amenity in [amen.id for amen in place.amenities] for amenity in amenities)]

    return jsonify([place.to_dict() for place in places])
