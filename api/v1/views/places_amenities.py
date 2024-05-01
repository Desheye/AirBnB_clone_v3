#!/usr/bin/python3
"""
Routes for handling linking between places and amenities
"""
from flask import jsonify, abort
from os import getenv

from api.v1.views import app_views, storage


@app_views.route("/places/<place_id>/amenities",
                 methods=["GET"],
                 strict_slashes=False)
def get_amenities_by_place(place_id):
    """
    Retrieve all amenities of a place
    :param place_id: ID of the place
    :return: JSON response containing all amenities
    """
    place = storage.get("Place", str(place_id))

    if place is None:
        abort(404)

    all_amenities = [amenity.to_json() for amenity in place.amenities]

    return jsonify(all_amenities)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def unlink_amenity_from_place(place_id, amenity_id):
    """
    Unlink an amenity from a place
    :param place_id: ID of the place
    :param amenity_id: ID of the amenity
    :return: Empty dictionary or error response
    """
    place = storage.get("Place", str(place_id))
    amenity = storage.get("Amenity", str(amenity_id))

    if place is None or amenity is None:
        abort(404)

    found = False

    for obj in place.amenities:
        if str(obj.id) == amenity_id:
            if getenv("HBNB_TYPE_STORAGE") == "db":
                place.amenities.remove(obj)
            else:
                place.amenity_ids.remove(obj.id)
            place.save()
            found = True
            break

    if not found:
        abort(404)
    else:
        return jsonify({}), 200


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["POST"],
                 strict_slashes=False)
def link_amenity_to_place(place_id, amenity_id):
    """
    Link an amenity to a place
    :param place_id: ID of the place
    :param amenity_id: ID of the amenity
    :return: JSON response with Amenity object added or error
    """
    place = storage.get("Place", str(place_id))
    amenity = storage.get("Amenity", str(amenity_id))

    if place is None or amenity is None:
        abort(404)

    if amenity in place.amenities:
        return jsonify(amenity.to_json()), 200

    if getenv("HBNB_TYPE_STORAGE") == "db":
        place.amenities.append(amenity)
    else:
        place.amenities = amenity

    place.save()

    return jsonify(amenity.to_json()), 201
