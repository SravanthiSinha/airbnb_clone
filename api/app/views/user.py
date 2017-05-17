"""
Manage the API routes to /users/*<user_id>
"""
from app.models.user import User
from flask_json import as_json, request
from app import app
from datetime import datetime
import json
from return_styles import ListStyle


@app.route('/users', methods=['GET'])
@as_json
def get_users():
    """
    Get all Users
    """
    data = User.select()
    return ListStyle.list(data, request), 200


@app.route('/users', methods=['POST'])
@as_json
def create_user():
    """
    Create a User
    """
    data = request.form
    try:
        if 'email' not in data:
            raise KeyError('email')
        if 'first_name' not in data:
            raise KeyError('first_name')
        if 'last_name' not in data:
            raise KeyError('last_name')
        if 'password' not in data:
            raise KeyError('password')
        email_check = User.select().where(User.email == data['email'])
        if email_check:
            return {'code': 10000, 'msg': 'Email already exists'}, 409

        user = User(
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name']
        )
        user.set_password(data['password'])
        user.save(force_insert=True)
        user.save
        res = {}
        res['code'] = 201
        res['msg'] = "User was created successfully"
        return res, 201
    except KeyError as e:
        res = {}
        res['code'] = 40000
        res['msg'] = 'Missing parameters'
        return res, 400
    except Exception as error:
        response = {}
        response['code'] = 403
        response['msg'] = str(error)
        return response, 403


@app.route('/users/<user_id>', methods=['GET'])
@as_json
def get_user(user_id):
    """
    Get a user with id as user_id
    """
    try:
        user = User.get(User.id == user_id)
    except Exception as error:
        response = {}
        response['code'] = 404
        response['msg'] = 'User not found'
        return response, 404
    return user.to_dict(), 200


@app.route('/users/<user_id>', methods=['PUT'])
@as_json
def update_user(user_id):
    """
    Update the user details of user with id as user_id
    """
    data = request.form
    user = User.get(User.id == user_id)
    try:
        for key in data:
            if key == 'email':
                raise Exception("Email cannot be changed")
            elif key == 'first_name':
                user.first_name = data['first_name']
            elif key == 'last_name':
                user.last_name = data['last_name']
            elif key == 'is_admin':
                user.is_admin = data['is_admin']
            elif key == 'password':
                user.set_password(data['password'])
        user.save()
        res = {}
        res['code'] = 200
        res['msg'] = "User was updated successfully"
        return res, 200
    except Exception as error:
        response = {}
        response['code'] = 403
        response['msg'] = str(error)
        return response, 403


@app.route('/users/<user_id>', methods=['DELETE'])
@as_json
def delete_user(user_id):
    """
    Delete user with id as user_id
    """
    try:
        user = User.get(User.id == user_id)
    except Exception as error:
        response = {}
        response['code'] = 404
        response['msg'] = 'User not found'
        return response, 404
    delete_user = User.delete().where(User.id == user_id)
    delete_user.execute()
    response = {}
    response['code'] = 200
    response['msg'] = "User was deleted successfully"
    return response, 200
