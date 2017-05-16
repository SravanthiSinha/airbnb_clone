"""
Unittest cases for the API routes to /users/*
"""

from datetime import datetime
import unittest
import json
import logging
from app.models.base import peewee_mysql_db as db
from app.models.user import User
from app import app


class UserTestCase(unittest.TestCase):

    table = User
    path = '/users'
    tablename = 'User'
    users = [
        {'first_name': 'Sravanthi', 'last_name': 'sinha',
         'email': 'sravanthi.sinha@holbertonschool.com',
         'password': '987654', 'is_admin': True},
        {'first_name': 'Tony', 'last_name': 'Stark',
         'email': 'tony@stark.com', 'password': '123456',
         'is_admin': False}]
    example = users[0]

    def setUp(self):
        self.app = app.test_client()
        logging.disable(logging.CRITICAL)
        db.create_tables([User], safe=True)

    def tearDown(self):
        db.drop_table(User)

    def check(self, value, expected):
        assert value == expected, self.errormsg(expected, value)

    def create_row(self, data, expec):
        resp = self.app.post(self.path, data=data)
        self.check(resp.status, expec)
        return self.table.select().order_by(self.table.id.desc()).get()

    def check_dupl_entry(self, data, code):
        last_entry = self.create_row(data, '409 CONFLICT')
        resp = self.app.post(self.path, data=data)
        data = json.loads(resp.data)
        self.check(data['code'], code)
        return last_entry

    # Auxiliary function to return error message for assert function
    def errormsg(self, expec, *got):
        return 'Expecting {} but got {}'.format(expec, got)

    # Auxiliary function for creation of user
    def create_user(self, user, expec):
        resp = self.app.post('/users', data=user)
        assert resp.status == expec, self.errormsg(expec, resp.status)
        return User.select().order_by(User.id.desc()).get()

    def test_create(self):
        without_email = {'first_name': 'Jony', 'last_name': 'Snow',
                         'password': '32145', 'is_admin': False}
        dupl_email = {'first_name': 'rose', 'last_name': 'Even',
                      'email': 'sravanthi.sinha@holbertonschool.com',
                      'password': '654', 'is_admin': True}

        count = 1
        for user in self.users:
            # It should create users with sequential ids.
            last_user = self.create_user(user, '201 CREATED')
            assert last_user.id == count, self.errormsg(count, last_user.id)
            count += 1
        # It should return bad request when email is not given.
        last_user = self.create_user(without_email, '400 BAD REQUEST')
        assert last_user.email == 'tony@stark.com', self.errormsg(
            'tony@stark.com', str(last_user.email))  # user not created
        # It should return 'CONFLICT' when using duplicated email.
        last_user = self.create_user(dupl_email, '409 CONFLICT')
        assert last_user.email == 'tony@stark.com',\
            self.errormsg('tony@stark.com', str(last_user.email))
        # It should return code 10000 when user's email is duplicated

    def test_list(self):
        # Get request to the User should return 0 when empty
        resp = self.app.get(self.path)
        data = json.loads(resp.data)
        self.check(resp.status_code, 200)
        # After item creation it should return the number of items
        self.create_row(self.example, '201 CREATED')
        resp = self.app.get(self.path)
        data = json.loads(resp.data)
        assert len(data) > 0, self.errormsg(1, len(data))

    def test_get(self):
        # Check the status code after create user(the assert is inside the
        # function create user)
        last_entry = self.create_row(self.example, '201 CREATED')
        resp = self.app.get('{}/{}'.format(self.path, last_entry.id))
        data = json.loads(resp.data)
        # Check that is the same resource as the creation
        self.check(data['id'], last_entry.id)
        # Check when the item doesn't exist
        resp = self.app.get('{}/42'.format(self.path))
        data = json.loads(resp.data)
        self.check(resp.status_code, 404)  # Check the http status code
        # Check returned msg
        self.check(data['msg'], '{} not found'.format(self.tablename))
        # Check returned code(from json response)
        self.check(data['code'], 404)

    def test_delete(self):
        last_entry = self.create_row(self.example, '201 CREATED')
        resp = self.app.get('{}/{}'.format(self.path, last_entry.id))
        data = json.loads(resp.data)
        # Check that is the same resource as the creation
        self.check(data['id'], last_entry.id)
        # It should delete the item by its ID
        resp = self.app.delete('{}/{}'.format(self.path, last_entry.id))
        data = json.loads(resp.data)
        self.check(data['msg'], 'User account was deleted')
        # It should return 404 for the delete item
        resp = self.app.get('{}/{}'.format(self.path, last_entry.id))
        self.check(resp.status_code, 404)
        # It should not be possible to delete item not in the database
        resp = self.app.delete('{}/42'.format(self.path))
        self.check(resp.status_code, 404)
        data = json.loads(resp.data)
        self.check(data['msg'], '{} not found'.format(self.tablename))

    def test_update(self):
        data = {'first_name': 'Philp', 'last_name': 'Edison'}
        # It should create an item
        last_entry = self.create_row(self.example, '201 CREATED')
        # It should return update message when the update was executed
        # successfully
        resp = self.app.put(
            '{}/{}'.format(self.path, last_entry.id), data=data)
        upd_stat = json.loads(resp.data)
        self.check(upd_stat['msg'], 'User was updated successfully')
        # The later request should show the updated item
        resp = self.app.get('{}/{}'.format(self.path, last_entry.id))
        upd_item = json.loads(resp.data)
        for key in data:
            self.check(upd_item[key], data[key])

        # It should give internal server error when trying to change email
        resp = self.app.put('{}/{}'.format(self.path, 1),
                            data={'email': 'rose@gmail.com'})
        self.check(resp.status_code, 403)
