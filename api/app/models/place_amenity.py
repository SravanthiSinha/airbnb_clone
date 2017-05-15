#!/usr/bin/python3
import peewee as pw
from base import *
from place import *
from amenity import *


class PlaceAmenities(pw.Model):
    place = ForeignKeyField(Place)
    amenity = ForeignKeyField(Amenity)

    class Meta:
        database = peewee_mysql_db
