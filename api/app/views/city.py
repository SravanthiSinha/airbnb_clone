"""
Manage the API routes to /state/*<state_id>/cities/*<city_id>
"""
from app.models.city import City
from app.models.city import State
from flask_json import as_json, request
from app import app
from datetime import datetime
import json


@app.route('/states/<state_id>/cities', methods=['GET'])
@as_json
def get_cities(state_id):
    """
    Get all cities
    """
    cities = []
    data = City.select().where(City.state == state_id)
    for row in data:
        cities.append(row.to_hash())
    return {"result": cities}, 200


@app.route('/states/<state_id>/cities', methods=['POST'])
@as_json
def create_city(state_id):
    """
    Create a city with state as state_id
    """
    data = request.form
    city_check = City.select().join(State).where(
        State.id == state_id, City.name == data['name'])
    if city_check:
        return {'code': 10000, 'msg': 'City already exists in this state'}, 409
    try:
        new = City.create(
            name=data['name'],
            state_id=state_id
        )
        res = {}
        res['code'] = 201
        res['msg'] = "City was created successfully"
        return res, 201
    except Exception as error:
        response = {}
        response['code'] = 403
        response['msg'] = str(error)
        return response, 403


@app.route('/states/<state_id>/cities/<city_id>', methods=['GET'])
@as_json
def get_city(state_id, city_id):
    """
    Get a city with id as place_id and state with  id as state_id
    """
    try:
        city = City.get(City.id == city_id, City.state == state_id)
    except Exception:
        return {'code': 404, 'msg': 'City not found'}, 404
    return city.to_hash(), 200


@app.route('/states/<s_id>/cities/<c_id>', methods=['DELETE'])
@as_json
def delete_city(s_id, c_id):
    """
    Delete city with id as place_id and state with  id as s_id
    """
    try:
        city = City.get(City.id == c_id, City.state == s_id)
    except Exception:
        return {'code': 404, 'msg': 'City not found'}, 404
    try:
        delete_city = City.delete().where(City.id == c_id, City.state == s_id)
        delete_city.execute()
        response = {}
        response['code'] = 200
        response['msg'] = "City was deleted successfully"
        return response, 200
    except Exception:
        response = {}
        response['code'] = 403
        response['msg'] = str(error)
        return response, 403
