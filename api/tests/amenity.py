"""
Unittest cases for the API routes to /amenity/*
"""
from base import BaseTestCase
from app.models.amenity import Amenity
from data import amenities
import unittest


class AmenitiesTestCase(BaseTestCase):
    table = [Amenity]
    path = '/amenities'
    example = amenities[0]

    def test_create(self):
        count = 1
        for amenity in amenities:
            last_amen = self.create_row(amenity, '201 CREATED')
            self.check(last_amen.id, count)
            count += 1

    def test_list(self):
        self.check_list()

    def test_get(self):
        self.check_get('Amenity')

    def test_delete(self):
        self.check_delete('Amenity')
