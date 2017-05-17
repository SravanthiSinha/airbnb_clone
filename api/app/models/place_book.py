"""
This is the place_book module.
This is a PlaceBook class inside the place_book module.
"""
from base import *
from place import *


class PlaceBook(BaseModel):
    """
    This is a PlaceBook class
    """
    place = ForeignKeyField(Place)
    user = ForeignKeyField(User, related_name='places_booked')
    is_validated = BooleanField(default=False)
    date_start = DateTimeField(null=False)
    number_nights = IntegerField(default=1)

    def to_dict(self):
        """
        Returns hash of the PlaceBook in the database
        """
        data = {}
        place = Place.get(Place.id == self.place)
        user = User.get(User.id == self.user)
        data['place_id'] = place.id
        data['user_id'] = user.id
        data['is_validated'] = self.is_validated
        data['date_start'] = self.date_start.strftime("%Y/%m/%d %H:%M:%S")
        data['number_nights'] = self.number_nights
        return super(PlaceBook, self).to_dict(self, data)
