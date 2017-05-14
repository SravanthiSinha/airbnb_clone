#!/usr/bin/python3
from config import *
from peewee import *

peewee_mysql_db = MySQLDatabase(DATABASE['database'])


class BaseModel(Model):
    class Meta:
        database = peewee_ mysql_db
        order_by = ("id", )

    id = IntegerField(unique=True, primary_key=True)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now
