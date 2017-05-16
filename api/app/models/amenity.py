from base import *
"""
This is the amenity module.
This is a Amenity class inside the amenity module.
"""


class Amenity(BaseModel):
    """
    This is a Amenity class
    """
    name = CharField(max_length=128, null=False)

    def to_hash(self):
        """
        Returns a hash of the Amenity in the database
        """
        data = {}
        data['name'] = self.name
        return super(Amenity, self).to_hash(self, data)
