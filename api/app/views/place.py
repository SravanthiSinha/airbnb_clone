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
from return_styles import ListStyle


@app.route('/places', methods=['GET'])
@as_json
def get_places():
    """
    Get all places
    """
    data = Place.select()
    return ListStyle.list(data, request), 200


@app.route('/places', methods=['POST'])
@as_json
def create_place():
    """
    Create a place
    """
    data = request.form
    try:
        if 'owner_id' not in data:
            raise KeyError('owner_id')
        if 'name' not in data:
            raise KeyError('name')
        if 'city_id' not in data:
            raise KeyError('city_id')
        new = Place.create(
            owner=data['owner_id'],
            name=data['name'],
            city=data['city_id'],
            description=data['description'],
            number_rooms=data['number_rooms'],
            number_bathrooms=data['number_bathrooms'],
            max_guest=data['max_guest'],
            price_by_night=data['price_by_night'],
            latitude=data['latitude'],
            longitude=data['longitude']
        )
    except KeyError as e:
        res = {}
        res['code'] = 40000
        res['msg'] = 'Missing parameters'
        return res, 400
    except Exception as error:
        res = {}
        res['code'] = 403
        print str(error)
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
    return place.to_dict(), 200


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
    data = Place.select().where(Place.city == city.id)
    return ListStyle.list(data, request), 200


@app.route('/states/<state_id>/cities/<city_id>/places', methods=['POST'])
@as_json
def create_place_by_city(state_id, city_id):
    """
    Create a place with id as place_id and state with  id as state_id
    """
    data = request.form
    try:
        if 'owner_id' not in data:
            raise KeyError('owner_id')
        if 'name' not in data:
            raise KeyError('name')

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
    except KeyError as e:
        res = {}
        res['code'] = 40000
        res['msg'] = 'Missing parameters'
        return res, 400


@app.route('/states/<state_id>/places', methods=['GET'])
@as_json
def get_places_by_state(state_id):
    """
    Get a place in a state with id as state_id
    """
    try:
        query = City.select().where(City.state == state_id)
        if not query.exists():
            return ListStyle.list(query, request), 200
        cities = []
        for city in query:
            cities.append(city.id)

        data = Place.select().where(Place.city << cities)
        return ListStyle.list(data, request), 200
    except Exception as e:
        res = {}
        res['code'] = 500
        res['msg'] = str(error)
        return res, 500


@app.route('/places/<place_id>/available', methods=['POST'])
@as_json
def check_place_available(place_id):
    """
    Check if place is available
    """
    data = request.form
    try:
        if 'year' not in data:
            raise KeyError('year')
        if 'month' not in data:
            raise KeyError('month')
        if 'day' not in data:
            raise KeyError('day')

        check_date = datetime(int(data['year']), int(
            data['month']), int(data['day']))

        bookings = PlaceBook.select().where(PlaceBook.place == place_id)
        for booking in bookings:
            date_start = booking.date_start.replace(hour=0, minute=0, second=0)
            date_end = date_start + timedelta(days=int(booking.number_nights))
            if check_date >= date_start and check_date < date_end:
                return {'available': False}, 200
        return {'available': True}, 200
    except KeyError as e:
        res = {}
        res['code'] = 40000
        res['msg'] = 'Missing parameters'
        return res, 400
    except Exception as e:
        res = {}
        res['code'] = 500
        res['msg'] = str(error)
        return res, 500
