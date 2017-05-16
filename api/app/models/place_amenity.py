"""
This is the place_amenity module.
This is a PlaceAmenities class inside the place_amenity module.
"""
import peewee as pw
from base import *
from place import *
from amenity import *


class PlaceAmenities(pw.Model):
    """
    This is a PlaceAmenities class
    """
    place = ForeignKeyField(Place)
    amenity = ForeignKeyField(Amenity)

    class Meta:
        database = peewee_mysql_db
