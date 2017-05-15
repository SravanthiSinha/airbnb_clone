from config import *
from peewee import *
import datetime

peewee_mysql_db = MySQLDatabase(DATABASE['database'],host=DATABASE['host'], charset=DATABASE['charset'], user=DATABASE['user'],
                                passwd=DATABASE['password'],port=DATABASE['port'])


class BaseModel(Model):
    id = IntegerField(unique=True, primary_key=True)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)
    database = peewee_mysql_db
    class Meta:
        database = peewee_mysql_db
        order_by = ("id", )

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now
