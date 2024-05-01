#!/usr/bin/python3
"""
Routes for handling Review objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.review import Review


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def get_reviews_by_place(place_id):
    """
    Retrieves all Review objects by place ID
    :return: JSON response containing all reviews
    """
    review_list = []
    place = storage.get("Place", str(place_id))

    if place is None:
        abort(404)

    for review in place.reviews:
        review_list.append(review.to_json())

    return jsonify(review_list)


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def create_review(place_id):
    """
    Creates a new Review object
    :return: Newly created Review object
    """
    review_json = request.get_json(silent=True)

    if review_json is None:
        abort(400, 'Not a JSON')

    if not storage.get("Place", place_id):
        abort(404)

    if not storage.get("User", review_json["user_id"]):
        abort(404)

    if "user_id" not in review_json:
        abort(400, 'Missing user_id')

    if "text" not in review_json:
        abort(400, 'Missing text')

    review_json["place_id"] = place_id

    new_review = Review(**review_json)
    new_review.save()

    resp = jsonify(new_review.to_json())
    resp.status_code = 201

    return resp


@app_views.route("/reviews/<review_id>",  methods=["GET"],
                 strict_slashes=False)
def get_review_by_id(review_id):
    """
    Retrieves a specific Review object by ID
    :param review_id: ID of the Review object
    :return: Review object with the specified ID or error response
    """

    review = storage.get("Review", str(review_id))

    if review is None:
        abort(404)

    return jsonify(review.to_json())


@app_views.route("/reviews/<review_id>",  methods=["PUT"],
                 strict_slashes=False)
def update_review(review_id):
    """
    Updates a specific Review object by ID
    :param review_id: ID of the Review object
    :return: Updated Review object with status code 200 on success,
             or error response with status code 400 or 404 on failure
    """
    review_json = request.get_json(silent=True)

    if review_json is None:
        abort(400, 'Not a JSON')

    review = storage.get("Review", str(review_id))

    if review is None:
        abort(404)

    for key, val in review_json.items():
        if key not in ["id", "created_at", "updated_at", "user_id",
                       "place_id"]:
            setattr(review, key, val)

    review.save()

    return jsonify(review.to_json())


@app_views.route("/reviews/<review_id>",  methods=["DELETE"],
                 strict_slashes=False)
def delete_review_by_id(review_id):
    """
    Deletes a Review object by ID
    :param review_id: ID of the Review object
    :return: Empty dictionary with status code 200 on success,
             or 404 if Review object is not found
    """

    review = storage.get("Review", str(review_id))

    if review is None:
        abort(404)

    storage.delete(review)
    storage.save()

    return jsonify({})
