"""
This is the review module.
This is a Review class inside the review module.
"""
from base import *
from user import *
from city import *


class Review(BaseModel):
    """
    This is a Review class
    """
    message = TextField()
    stars = IntegerField(default=0)
    user = ForeignKeyField(User, related_name='reviews', on_delete="CASCADE")

    def to_hash(self):
        """
        Returns hash of the Review in the database
        """
        data = {}
        data['message'] = self.message
        data['stars'] = self.stars
        data['fromuserid'] = self.user_id
        if 'reviewuser' in dir(self):
            data['touserid'] = self.reviewuser.user_id
        else:
            data['touserid'] = None
        if 'reviewplace' in dir(self):
            data['toplaceid'] = self.reviewplace.place_id
        else:
            data['toplaceid'] = None
        return super(Review, self).to_hash(self, data)
