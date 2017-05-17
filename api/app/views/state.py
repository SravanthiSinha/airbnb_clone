"""
Manage the API routes to /states/*<state_id>
"""
from app.models.state import State
from flask_json import as_json, request
from app import app
from datetime import datetime
import json
from return_styles import ListStyle


@app.route('/states', methods=['GET'])
@as_json
def get_states():
    """
    Get all states
    """
    data = State.select()
    return ListStyle.list(data, request), 200


@app.route('/states', methods=['POST'])
@as_json
def create_state():
    """
    Create a state
    """
    data = request.form
    try:
        if 'name' not in data:
            raise KeyError('name')

        state_check = State.select().where(State.name == data['name'])
        new = State.create(name=data['name'])
        res = {}
        res['code'] = 201
        res['msg'] = "State was created successfully"
        return res, 201
    except KeyError as e:
        response = {}
        response['code'] = 40000
        response['msg'] = 'Missing parameters'
        return response, 400
    except Exception as e:
        response = {}
        response['code'] = 10001
        response['msg'] = "State already exists"
        return response, 409


@app.route('/states/<state_id>', methods=['GET'])
@as_json
def get_state(state_id):
    """
    Get a state with id as state_id
    """
    try:
        state = State.get(State.id == state_id)
    except Exception as error:
        response = {}
        response['code'] = 404
        response['msg'] = 'State not found'
        return response, 404
    return state.to_dict(), 200


@app.route('/states/<state_id>', methods=['DELETE'])
@as_json
def delete_state(state_id):
    """
    Delete state with id as state_id
    """
    try:
        state = State.get(State.id == state_id)
    except Exception as error:
        response = {}
        response['code'] = 404
        response['msg'] = 'State not found'
        return response, 404
    delete_state = State.delete().where(State.id == state_id)
    delete_state.execute()
    response = {}
    response['code'] = 200
    response['msg'] = "State was deleted successfully"
    return response, 200
