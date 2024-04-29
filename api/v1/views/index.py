#!/usr/bin/python3
"""
This module defines the index routes for the AirBnB clone project.
"""

from flask import jsonify
from api.v1.views import app_views

from models import storage


@app_views.route("/status", methods=['GET'], strict_slashes=False)
def get_status():
    """
    Route to retrieve the status of the API.
    :return: JSON response containing the API status
    """
    status_data = {
        "status": "OK"
    }

    response = jsonify(status_data)
    response.status_code = 200

    return response


@app_views.route("/stats", methods=['GET'], strict_slashes=False)
def get_stats():
    """
    Route to retrieve statistics of all objects.
    :return: JSON response containing statistics of all objects
    """
    statistics_data = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User"),
    }

    response = jsonify(statistics_data)
    response.status_code = 200

    return response
