"""
Unittest cases for the API routes to /users/*<user_id>/reviews/*<review_id>
"""
from app import app
from app.models.review import Review
from app.models.review_place import ReviewPlace
from app.models.review_user import ReviewUser
from app.models.user import User
from app.models.place import Place
from flask_json import as_json, request
from datetime import datetime
from flask import abort
import json


@app.route('/users/<user_id>/reviews', methods=['GET'])
@as_json
def get_user_reviews(user_id):
    """
    Get user Reviews of user with id as user_id
    """
    try:
        query = User.select().where(User.id == user_id)
        if not query.exists():
            raise LookupError('user_id')
        reviews = ReviewUser.select().where(ReviewUser.user == user_id)
        results = []
        for review in reviews:
            result = Review.get(Review.id == review.review)
            data = result.to_hash()
            data['touserid'] = int(user_id)
            results.append(data)

        return {'result': results}, 200
    except LookupError as e:
        abort(404)
    except Exception as e:
        res = {
            'code': 500,
            'msg': e.message
        }
        return res, 500


@app.route('/users/<user_id>/reviews', methods=['POST'])
@as_json
def create_user_reviews(user_id):
    """
    Create User Reviews of user with id as user_id
    """
    data = request.form
    try:
        if not data['user_id']:
            raise KeyError('user_id')
        elif not data['message']:
            raise KeyError('message')
        elif not isinstance(data['message'], unicode):
            raise ValueError('message')
        query = User.select().where(User.id == user_id)
        if not query.exists():
            raise LookupError('user_id')
        query = User.select().where(User.id == data['user_id'])
        if not query.exists():
            raise LookupError('from_user_id')
        new_review = Review(
            user_id=data['user_id'],
            message=data['message']
        )
        if 'stars' in data:
            new_review.stars = data['stars']
        new_review.save()
        new_user_review = ReviewUser.create(
            user=user_id,
            review=new_review.id
        )
        res = {}
        res['code'] = 201
        res['msg'] = 'Review was saved successfully'
        res['id'] = new_review.id
        return res, 201
    except KeyError as e:
        res = {}
        res['code'] = 400
        res['msg'] = str(e.message) + ' is missing'
        return res, 400
    except ValueError as e:
        res = {}
        res['code'] = 400
        res['msg'] = str(e.message) + ' is invalid'
        return res, 400
    except LookupError as e:
        abort(404)
    except Exception as e:
        res = {}
        res['code'] = 500
        res['msg'] = e.message
        return res, 500


@app.route('/users/<user_id>/reviews/<review_id>', methods=['GET'])
@as_json
def get_user_review(user_id, review_id):
    """
    Create User Reviews of user with id as user_id and review with id as reveiw_id
    """
    try:
        query = ReviewUser.select().where(
            ReviewUser.review == review_id,
            ReviewUser.user == user_id)
        if not query.exists():
            raise LookupError('Review not found')
        query = Review.get(Review.id == review_id)
        data = query.to_hash()
        data['touserid'] = user_id
        return data, 200
    except LookupError as e:
        abort(404)
    except Exception as e:
        return e, 409


@app.route('/users/<user_id>/reviews/<review_id>', methods=['DELETE'])
@as_json
def delete_user_review(user_id, review_id):
    """
    Delete User Reviews of user with id as user_id and review with id as reveiw_id
    """
    try:
        query = ReviewUser.select().where(
            ReviewUser.review == review_id,
            ReviewUser.user == user_id)
        if not query.exists():
            raise LookupError('Review not found')
        query = Review.select().where(Review.id == review_id)
        if not query.exists():
            raise LookupError('Review not found')
        ReviewUser.delete().where(
            ReviewUser.review == review_id,
            ReviewUser.user == user_id).execute()
        Review.delete().where(Review.id == review_id).execute()
        res = {
            'code': 200,
            'msg': 'Review was deleted successfully'
        }
        return res, 200
    except LookupError as e:
        abort(404)
    except Exception as e:
        return e, 409


@app.route('/places/<place_id>/reviews', methods=['GET'])
@as_json
def get_place_reviews(place_id):
    try:
        query = Place.select().where(Place.id == place_id)
        if not query.exists():
            raise LookupError('place_id')
        reviews = ReviewPlace.select().where(ReviewPlace.place == place_id)
        results = []
        for review in reviews:
            result = Review.get(Review.id == review.review)
            data = result.to_hash()
            data['toplaceid'] = int(place_id)
            results.append(data)
        return {'result': results}, 200
    except LookupError as e:
        abort(404)
    except Exception as e:
        res = {
            'code': 500,
            'msg': e.message
        }
        return res, 500


@app.route('/places/<place_id>/reviews', methods=['POST'])
@as_json
def create_place_review(place_id):
    data = request.form
    try:
        if not data['user_id']:
            raise KeyError('user_id')
        elif not data['message']:
            raise KeyError('message')
        elif not isinstance(data['message'], unicode):
            raise ValueError('message')
        query = Place.select().where(Place.id == place_id)
        if not query.exists():
            raise LookupError('place_id')
        query = User.select().where(User.id == data['user_id'])
        if not query.exists():
            raise LookupError('user_id')
        new_review = Review(
            user_id=data['user_id'],
            message=data['message']
        )
        if 'stars' in data:
            new_review.stars = data['stars']
        new_review.save()
        new_place_review = ReviewPlace.create(
            place=place_id,
            review=new_review.id
        )
        res = {}
        res['code'] = 201
        res['msg'] = 'Review was saved successfully'
        res['id'] = new_review.id
        return res, 201
    except KeyError as e:
        res = {}
        res['code'] = 400
        res['msg'] = str(e.message) + ' is missing'
        return res, 400
    except ValueError as e:
        res = {}
        res['code'] = 400
        res['msg'] = str(e.message) + ' is invalid'
        return res, 400
    except LookupError as e:
        abort(404)
    except Exception as e:
        res = {}
        res['code'] = 500
        res['msg'] = e.message
        return res, 500


@app.route('/places/<place_id>/reviews/<review_id>', methods=['GET'])
@as_json
def get_place_review(place_id, review_id):
    try:
        query = ReviewPlace.select().where(
            ReviewPlace.review == review_id,
            ReviewPlace.place == place_id)
        if not query.exists():
            raise LookupError('Review not found')
        query = Review.get(Review.id == review_id)
        data = query.to_hash()
        data['toplaceid'] = place_id
        return data, 200
    except LookupError as e:
        abort(404)
    except Exception as e:
        return e, 409


@app.route('/places/<place_id>/reviews/<review_id>', methods=['DELETE'])
@as_json
def delete_place_review(place_id, review_id):
    try:
        query = ReviewPlace.select().where(
            ReviewPlace.review == review_id,
            ReviewPlace.place == place_id)
        if not query.exists():
            raise LookupError('Review not found')
        query = Review.select().where(Review.id == review_id)
        if not query.exists():
            raise LookupError('Review not found')
        ReviewPlace.delete().where(
            ReviewPlace.review == review_id,
            ReviewPlace.place == place_id).execute()
        Review.delete().where(Review.id == review_id).execute()
        res = {
            'code': 200,
            'msg': 'Review was deleted successfully'
        }
        return res, 200
    except LookupError as e:
        abort(404)
    except Exception as e:
        return e, 409
