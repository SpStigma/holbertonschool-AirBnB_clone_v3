#!/usr/bin/python3
"""Reviews"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_place_reviews(place_id):
    """Retrieves the list of all Review objects of a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=["GET"])
def get_review(review_id):
    """Retrieves a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    else:
        return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """Deletes a Review object with id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    else:
        storage.delete(review)
        storage.save()

    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Creates a new Review"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)
    if 'text' not in data:
        abort(400, 'Missing text')

    new_review = Review(place_id=place_id, **data)
    storage.new(new_review)
    storage.save()

    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"])
def update_review(review_id):
    """Updates a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    else:
        request_http = request.get_json()
        if request_http is None:
            abort(400, 'Not a JSON')

    for key, value in request_http.items():
        if key not in ['id', 'user_id', 'place_id',
                       'created_at', 'updated_at']:
            setattr(review, key, value)

    storage.save()

    return jsonify(review.to_dict()), 200
