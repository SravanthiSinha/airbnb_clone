"""
This is the base module.
This is a BaseModel class inside the base module.
"""
from config import *
from peewee import *
from datetime import datetime

peewee_mysql_db = MySQLDatabase(host=DATABASE["host"],
                                port=DATABASE["port"],
                                user=DATABASE["user"],
                                password=DATABASE["password"],
                                database=DATABASE["database"])


class BaseModel(Model):
    """
    This is a BaseModel class
    """
    id = PrimaryKeyField(unique=True)
    created_at = DateTimeField(
        default=datetime.now(),
        formats="%d/%m/%Y %H:%M:%S")
    updated_at = DateTimeField(
        default=datetime.now(),
        formats="%d/%m/%Y %H:%M:%S")

    class Meta:
        database = peewee_mysql_db
        order_by = ("id", )

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        super(BaseModel, self).save()

    def to_hash(model, self, data):
        """
        Returns a hash of the BaseModel in the database
        """
        data['id'] = self.id
        data['created_at'] = self.created_at.strftime("%Y/%m/%d %H:%M:%S")
        data['updated_at'] = self.updated_at.strftime("%Y/%m/%d %H:%M:%S")
        return data
