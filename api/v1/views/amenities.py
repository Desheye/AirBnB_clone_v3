#!/usr/bin/python3

"""
Module for managing amenity operations.
"""

from flask import jsonify, abort, request
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views


@app_views.route('/amenities', strict_slashes=False)
def retrieve_all_amenities():
    """
    Retrieves a list of amenities.
    """
    amenity_list = []
    for amenity in storage.all(Amenity).values():
        amenity_list.append(amenity.to_dict())
    return jsonify(amenity_list)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def retrieve_amenity(amenity_id):
    """
    Retrieves an amenity object by its ID.
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    else:
        return abort(404)


@app_views.route('/amenities/<amenity_id>',
                 methods=["DELETE"], strict_slashes=False)
def delete_amenity(amenity_id):
    """
    Deletes an amenity object by its ID.
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    else:
        return abort(404)


@app_views.route('/amenities', methods=["POST"], strict_slashes=False)
def create_amenity():
    """
    Creates a new amenity object.
    """
    if request.content_type != 'application/json':
        return abort(400, "Not a JSON")
    if not request.get_json():
        return abort(400, "Not a JSON")
    data = request.get_json()

    if 'name' not in data:
        return abort(400, "Missing Name")

    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities', methods=["PUT"], strict_slashes=False)
def add_amenity():
    """
    Adds a new amenity object.
    """
    if request.content_type != 'application/json':
        return abort(400, "Not a JSON")
    if not request.get_json():
        return abort(400, "Not a JSON")
    data = request.get_json()

    if 'name' not in data:
        return abort(400, "Missing Name")

    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 200


@app_views.route('/amenities/<amenity_id>',
                 methods=["PUT"], strict_slashes=False)
def update_amenity(amenity_id):
    """
    Updates an amenity object by its ID.
    """
    if request.content_type != 'application/json':
        return abort(400, "Not a JSON")
    if not request.get_json():
        return abort(400, "Not a JSON")
    data = request.get_json()

    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        ignore_keys = ['id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(amenity, key, value)
        amenity.save()
        return jsonify(amenity.to_dict()), 200
    else:
        return abort(404)
