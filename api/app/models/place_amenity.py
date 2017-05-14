#!/usr/bin/python3
from peewee import *
from BaseModel import *


class PlaceAmenities(Model):
    place = ForeignKeyField(Place)
    amenity = ForeignKeyField(Amenity)

    class Meta:
        database = peewee_mysql_db
