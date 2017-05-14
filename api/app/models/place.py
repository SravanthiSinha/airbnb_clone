#!/usr/bin/python3
from base import *


class Place(BaseModel):
    owner = ForeignKeyField(User, related_name='places')
    city = ForeignKeyField(City, related_name='places')
    name = CharField(max_length=128, null=False)
    description = TextField()
    number_rooms = IntegerField(default=0)
    number_bathrooms = IntegerField(default=0)
    max_guest = IntegerField(default=0)
    price_by_night = IntegerField(default=0)
    latitude = FloatField()
    longitude = FloatField()
