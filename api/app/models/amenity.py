from base import *


class Amenity(BaseModel):
    name = CharField(max_length=128, null=False)
