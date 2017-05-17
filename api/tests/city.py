"""
Unittest cases for the API routes to /states/*<state_id>/cities/*<city_id>
"""
from base import BaseTestCase
from app.models.city import City
from app.models.state import State
from data import cities, states


class CityTestCase(BaseTestCase):
    table = [State, City]
    path = '/states/1/cities'

    example = cities[0]

    def create_states(self):
        state_table = {'model': State, 'path': '/states'}
        for state in states:
            last_state = self.create(state_table, state)

    def test_create(self):
        self.create_states()
        count = 1

        for city in cities:
            # It should create users with sequential ids.
            last_city = self.create_row(city, '201 CREATED')
            self.check(last_city.id, count)
            count += 1

        # It should return code 10000 when trying to create city with
        # duplicated namne
        last_city = self.check_dupl_entry({'name': 'San Francisco'}, 10000)
        self.check(last_city.name, 'San Francisco')

    def test_list(self):
        self.create_states()
        self.check_list()

    def test_get(self):
        self.create_states()
        self.check_get('City')

    def test_delete(self):
        self.create_states()
        self.check_delete('City')
