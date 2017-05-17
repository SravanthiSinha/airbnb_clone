"""
Unittest cases for the API routes to /places/*<place_id>/books/*<book_id>
"""
from base import BaseTestCase
from app.models.place_book import PlaceBook
from app.models.user import User
from app.models.place import Place
from app.models.state import State
from app.models.city import City
from data import *


class PlaceBookTestCase(BaseTestCase):
    table = [User, State, City, Place, PlaceBook]
    path = '/places/1/books'
    example = pbooks[0]

    def create_places_users(self):
        self.create_states_and_cities()
        place_table = {'model': Place, 'path': '/places'}
        user_table = {'model': User, 'path': '/users'}
        for user in users:
            last_user = self.create(user_table, user)
            self.check(last_user.email, user['email'])
        for place in places:
            last_place = self.create(place_table, place)
            self.check(last_place.name, place['name'])

    def test_create(self):
        self.create_places_users()
        count = 1
        for pb in pbooks:
            last_pbook = self.create_row(pb, '201 CREATED')
            self.check(last_pbook.id, count)
            count += 1

    def test_list(self):
        self.create_places_users()
        self.check_list()

    def test_get(self):
        self.create_places_users()
        self.check_get('Booking')

    def test_update(self):
        self.create_places_users()
        upd_data = {
            'date_start': '2016/07/20 09:01:10',
            'is_validated': True,
            'number_nights': 10}
        self.check_update(upd_data, 'Booking')

    def test_delete(self):
        self.create_places_users()
        self.check_delete('Booking')
