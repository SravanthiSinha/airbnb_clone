import unittest
import logging
import json
from app.models.base import peewee_mysql_db as database
from app.models.state import State
from app.models.user import User
from app.models.city import City
from app import app
from data import states, cities, users


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        logging.disable(logging.CRITICAL)
        database.create_tables(self.table, safe=True)

    def tearDown(self):
        for db in reversed(self.table):
            database.drop_table(db)

    def errormsg(self, expec, *got):
        return 'Expecting {} but got {}'.format(expec, got)

    def check(self, value, expected):
        assert value == expected, self.errormsg(expected, value)

    def create_row(self, data, expec):
        resp = self.app.post(self.path, data=data)
        self.check(resp.status, expec)
        return self.table[-1].select().order_by(self.table[-1].id.desc()).get()

    def create(self, table, data):
        resp = self.app.post(table['path'], data=data)
        self.check(resp.status, '201 CREATED')
        return table['model'].select().order_by(table['model'].id.desc()).get()

    def check_dupl_entry(self, data, code):
        last_entry = self.create_row(data, '409 CONFLICT')
        resp = self.app.post(self.path, data=data)
        data = json.loads(resp.data)
        self.check(data['code'], code)
        return last_entry

    def check_list(self):
        # Get request to the table should return 0 when empty
        resp = self.app.get(self.path)
        data = json.loads(resp.data)
        self.check(resp.status, "200 OK")
        # After item creation it should return the number of items
        self.create_row(self.example, '201 CREATED')
        resp = self.app.get(self.path)
        data = json.loads(resp.data)
        assert len(data) > 0, self.errormsg(1, len(data))

    def check_get(self, tname):
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
        self.check(data['msg'], '{} not found'.format(tname))
        # Check returned code(from json response)
        self.check(data['code'], 404)

    def check_delete(self, tname):
        last_entry = self.create_row(self.example, '201 CREATED')
        resp = self.app.get('{}/{}'.format(self.path, last_entry.id))
        data = json.loads(resp.data)
        # Check that is the same resource as the creation
        self.check(data['id'], last_entry.id)
        # It should delete the item by its ID
        resp = self.app.delete('{}/{}'.format(self.path, last_entry.id))
        data = json.loads(resp.data)
        self.check(data['msg'], '{} was deleted successfully'.format(tname))
        # It should return 404 for the delete item
        resp = self.app.get('{}/{}'.format(self.path, last_entry.id))
        self.check(resp.status_code, 404)
        # It should not be possible to delete item not in the database
        resp = self.app.delete('{}/42'.format(self.path))
        self.check(resp.status_code, 404)
        data = json.loads(resp.data)
        self.check(data['msg'], '{} not found'.format(tname))

    def check_update(self, data, tname):
        # It should create an item
        last_entry = self.create_row(self.example, '201 CREATED')
        # It should return update message when the update was executed
        # successfully
        resp = self.app.put(
            '{}/{}'.format(self.path, last_entry.id), data=data)
        upd_stat = json.loads(resp.data)
        self.check(
            upd_stat['msg'],
            '{} was updated successfully'.format(tname))
        # The later request should show the updated item
        resp = self.app.get('{}/{}'.format(self.path, last_entry.id))
        upd_item = json.loads(resp.data)
        for key in data:
            self.check(upd_item[key], data[key])

    def create_states_and_cities(self):
        state_table = {'model': State, 'path': '/states'}
        city_table = {'model': City, 'path': '/states/1/cities'}
        for state in states:
            last_state = self.create(state_table, state)
        for city in cities:
            last_city = self.create(city_table, city)
        return (last_state, last_city)

    def create_users(self):
        user_table = {'model': User, 'path': '/users'}
        for user in users:
            last_user = self.create(user_table, user)
        return last_user
