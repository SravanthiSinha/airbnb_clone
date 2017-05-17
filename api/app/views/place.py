"""
Manage the API routes to /places/*<place_id>
"""
from app.models.place import Place
from app.models.city import City
from app.models.state import State
from flask_json import as_json, request
from app import app
from datetime import datetime
import json


@app.route('/places', methods=['GET'])
@as_json
def get_places():
    """
    Get all places
    """
    places = []
    data = Place.select()
    for row in data:
        places.append(row.to_hash())
    return {"result": places}, 200


@app.route('/places', methods=['POST'])
@as_json
def create_place():
    """
    Create a place
    """
    data = request.form
    try:
        new = Place.create(
            owner=data['owner'],
            name=data['name'],
            city=data['city'],
            description=data['description'],
            number_rooms=data['number_rooms'],
            number_bathrooms=data['number_bathrooms'],
            max_guest=data['max_guest'],
            price_by_night=data['price_by_night'],
            latitude=data['latitude'],
            longitude=data['longitude']
        )
    except Exception as error:
        res = {}
        res['code'] = 403
        res['msg'] = str(error)
        return res, 403
    res = {}
    res['code'] = 201
    res['msg'] = "Place was created successfully"
    return res, 201


@app.route('/places/<place_id>', methods=['GET'])
@as_json
def get_place(place_id):
    """
    Get a place with id as place_id
    """
    try:
        place = Place.get(Place.id == place_id)
    except Exception:
        return {'code': 404, 'msg': 'Place not found'}, 404
    return place.to_hash(), 200


@app.route('/places/<place_id>', methods=['PUT'])
@as_json
def update_place(place_id):
    """
    Update the place details of place with id as place_id
    """
    data = request.form
    try:
        place = Place.get(Place.id == place_id)
        for key in data:
            if key == 'owner':
                raise Exception('Owner cannot be changed')
            elif key == 'city':
                raise Exception('City cannot be changed')
            elif key == 'name':
                place.name = data[key]
            elif key == 'description':
                place.description = data[key]
            elif key == 'number_rooms':
                place.number_rooms = data[key]
            elif key == 'number_bathrooms':
                place.number_bathrooms = data[key]
            elif key == 'max_guest':
                place.max_guest = data[key]
            elif key == 'price_by_night':
                place.price_by_night = data[key]
            elif key == 'latitude':
                place.latitude = data[key]
            elif key == 'longitude':
                place.longitude = data[key]
        place.save()
        res = {}
        res['code'] = 200
        res['msg'] = "Place was updated successfully"
        return res, 200
    except Exception as error:
        res = {}
        res['code'] = 403
        res['msg'] = str(error)
        return res, 403


@app.route('/places/<place_id>', methods=['DELETE'])
@as_json
def delete_place(place_id):
    """
    Delete place with id as place_id
    """
    try:
        place = Place.get(Place.id == place_id)
    except Exception:
        return {'code': 404, 'msg': 'Place not found'}, 404
    delete_place = Place.delete().where(Place.id == place_id)
    delete_place.execute()
    response = {}
    response['code'] = 200
    response['msg'] = "Place was deleted successfully"
    return response, 200


@app.route('/states/<state_id>/cities/<city_id>/places', methods=['GET'])
@as_json
def get_places_by_city(state_id, city_id):
    """
    Get a place with id as place_id and state with  id as state_id
    """
    city = City.get(City.id == city_id, City.state == state_id)
    places = []
    data = Place.select().where(Place.city == city.id)
    for row in data:
        places.append(row.to_hash())
    return {"result": places}, 200


@app.route('/states/<state_id>/cities/<city_id>/places', methods=['POST'])
@as_json
def create_place_by_city(state_id, city_id):
    """
    Create a place with id as place_id and state with  id as state_id
    """
    data = request.form
    city = City.get(City.id == city_id, City.state == state_id)
    new = Place.create(
        owner=data['owner_id'],
        name=data['name'],
        city=city.id,
        description=data['description'],
        number_rooms=data['number_rooms'],
        number_bathrooms=data['number_bathrooms'],
        max_guest=data['max_guest'],
        price_by_night=data['price_by_night'],
        latitude=data['latitude'],
        longitude=data['longitude']
    )
    res = {}
    res['code'] = 201
    res['msg'] = "Place was created successfully"
    return res, 201
