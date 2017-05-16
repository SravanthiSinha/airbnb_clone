"""
Manage the API routes to  /amenities/*
"""
from app.models.amenity import Amenity
from app.models.place_amenity import PlaceAmenities
from flask_json import as_json, request
from app import app
from datetime import datetime
import json


@app.route('/amenities', methods=['GET'])
@as_json
def get_amenities():
    """
    Get all amenities
    """
    amenities = []
    data = Amenity.select()
    for row in data:
        amenities.append(row.to_hash())
    return {"result": amenities}, 200


@app.route('/amenities', methods=['POST'])
@as_json
def create_amenity():
    """
    Create a amenity
    """
    data = request.form
    check_amenity = Amenity.select(). where(Amenity.name == data['name'])
    if check_amenity:
        return {'code': 10003, 'msg': 'Name already exists'}, 409

    try:
        new = Amenity.create(
            name=data['name']
        )
        res = {}
        res['code'] = 201
        res['msg'] = "Amenity was created successfully"
        return res, 201
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
    return amenity.to_hash(), 200


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


@app.route('/places/<place_id>/amenities', methods=['GET'])
@as_json
def get_place_amenities(place_id):
    """
    Get amenities with id as place_id
    """
    amenities = []
    data = PlaceAmenities.select().where(PlaceAmenities.place == place_id)
    for row in data:
        amenity = Amenity.get(Amenity.id == row.amenity)
        amenities.append(amenity.to_hash)
    return {"result": amenities}, 200
