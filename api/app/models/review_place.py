"""
This is the review_place module.
This is a ReviewPlace class inside the review_place module.
"""
from peewee import *
from base import *
from review import *
from place import *


class ReviewPlace(Model):
    """
    This is a ReviewPlace class
    """
    place = ForeignKeyField(Place)
    review = ForeignKeyField(Review)

    class Meta:
        database = peewee_mysql_db
