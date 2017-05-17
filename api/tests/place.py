"""
Unittest cases for the API routes to /places/*
"""
from base import BaseTestCase
from app.models.place import Place
from app.models.state import State
from app.models.city import City
from app.models.user import User
from data import *
import unittest


class PlaceTestCase(BaseTestCase):
    table = [User, State, City, Place]
    path = '/places'
    example = places[0]

    def test_cities(self):
        last_state, last_city = self.create_states_and_cities()
        self.check(last_state.name, states[-1]['name'])
        self.check(last_city.name, cities[-1]['name'])
        city = City.get(City.id == 3, City.state == 1)
        self.check(cities[2]['name'], city.name)

    def test_users(self):
        last_user = self.create_users()
        self.check(last_user.email, users[-1]['email'])

    def test_create(self):
        self.create_states_and_cities()
        self.create_users()
        count = 1
        for place in places:
            # It should create a place with sequential ids.
            last_place = self.create_row(place, '201 CREATED')
            self.check(last_place.id, count)
            count += 1

        # It should return 400 BAD REQUEST.
        last_place = self.create_row(place_br, '400 BAD REQUEST')
        self.check(last_place.id, 2)

    def test_list(self):
        self.create_states_and_cities()
        self.create_users()
        self.check_list()

    def test_get(self):
        self.create_states_and_cities()
        self.create_users()
        self.check_get('Place')

    def test_delete(self):
        self.create_states_and_cities()
        self.create_users()
        self.check_delete('Place')

    def test_update(self):
        self.create_states_and_cities()
        self.create_users()
        upd_data = {'name': 'Marriott', 'number_bathrooms': 2, 'max_guest': 10}
        self.check_update(upd_data, 'Place')
