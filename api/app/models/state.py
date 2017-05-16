"""
This is the state module.
This is a State class inside the state module.
"""
from base import *


class State(BaseModel):
    """
    This is a State class
    """
    name = CharField(max_length=128, null=False, unique=True)

    def to_hash(self):
        """
        Returns hash of the State in the database
        """
        data = {}
        data['name'] = self.name
        return super(State, self).to_hash(self, data)
