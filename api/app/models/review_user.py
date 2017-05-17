"""
This is the review_user module.
This is a ReviewUser class inside the review_user module.
"""
from peewee import *
from base import *
from review import *
from user import *


class ReviewUser(Model):
    """
    This is a ReviewUser class
    """
    user = ForeignKeyField(User)
    review = ForeignKeyField(Review)

    class Meta:
        database = peewee_mysql_db
