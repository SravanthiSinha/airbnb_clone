"""
Manage the API routes to  /amenities/*
"""
from app.models.amenity import Amenity
from app.models.place_amenity import PlaceAmenities
from flask_json import as_json, request
from app import app
from datetime import datetime
import json
from return_styles import ListStyle


@app.route('/amenities', methods=['GET'])
@as_json
def get_amenities():
    """
    Get all amenities
    """
    data = Amenity.select()
    return ListStyle.list(data, request), 200


@app.route('/amenities', methods=['POST'])
@as_json
def create_amenity():
    """
    Create a amenity
    """
    data = request.form
    try:
        if 'name' not in data:
            raise KeyError("'name'")

        check_amenity = Amenity.select(). where(Amenity.name == data['name'])
        if check_amenity:
            return {'code': 10003, 'msg': 'Name already exists'}, 409

        new = Amenity.create(
            name=data['name']
        )
        res = {}
        res['code'] = 201
        res['msg'] = "Amenity was created successfully"
        return res, 201
    except KeyError as e:
        res = {}
        res['code'] = 40000
        res['msg'] = 'missing parameters'
        return res, 400
    except Exception as error:
        response = {}
        response['code'] = 409
        response['msg'] = str(error)
        return response, 409


@app.route('/amenities/<amenity_id>', methods=['GET'])
@as_json
def get_amenity(amenity_id):
    """
    Get a amenity with id as amenity_id
    """
    try:
        amenity = Amenity.get(Amenity.id == amenity_id)
    except Exception:
        return {'code': 404, 'msg': 'Amenity not found'}, 404
    return amenity.to_dict(), 200


@app.route('/amenities/<amenity_id>', methods=['DELETE'])
@as_json
def delete_amenity(amenity_id):
    """
    Delete amenity with id as amenity_id
    """
    try:
        amenity = Amenity.get(Amenity.id == amenity_id)
    except Exception:
        return {'code': 404, 'msg': 'Amenity not found'}, 404
    amenity = Amenity.delete().where(Amenity.id == amenity_id)
    amenity.execute()
    res = {}
    res['code'] = 201
    res['msg'] = "Amenity was deleted successfully"
    return res, 201


@app.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'])
@as_json
def create_place_amenities(place_id, amenity_id):
    """
    Create a amenity
    """
    data = request.form
    check_amenity = PlaceAmenities.select().where(
        PlaceAmenities.amenity == amenity_id,
        PlaceAmenities.place == place_id)
    if check_amenity:
        return {'code': 10003,
                'msg': 'Amenity is already set for the given place'}, 409

    try:
        new = PlaceAmenities.create(place=place_id, amenity=amenity_id)
        res = {}
        res['code'] = 201
        res['msg'] = "Amenity was created successfully"
        return res, 201
    except Exception as error:
        response = {}
        response['code'] = 409
        response['msg'] = str(error)
        return response, 409


@app.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'])
@as_json
def delete_place_amenities(place_id, amenity_id):
    """
    Delete amenities with id as amenity_id and place with id as place_id
    """
    try:
        delete = PlaceAmenities.delete().where(
            PlaceAmenities.amenity == amenity_id,
            PlaceAmenities.place == place_id
        )
        delete.execute()
        res = {}
        res['code'] = 200
        res['msg'] = 'Amenity deleted successfully'
        return res, 200
    except Exception as error:
        response = {}
        response['code'] = 409
        response['msg'] = str(error)
        return response, 409
