#!/usr/bin/python3
from base import *


class City(BaseModel):
    name = CharField(max_length=128, null=False)
    state = ForeignKeyField(State, related_name='cities', cascade=True)
