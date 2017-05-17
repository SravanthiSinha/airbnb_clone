from app.models.base import peewee_mysql_db as db
from app.models.user import *
from app.models.state import *
from app.models.city import *
from app.models.place import *
from app.models.place_book import *
from app.models.amenity import *
from app.models.place_amenity import *
from app.models.review import *
from app.models.review_user import *
from app.models.review_place import *


''' Create each table in the database '''
db.connect()
db.create_tables([User,
                  State,
                  City,
                  Place,
                  PlaceBook,
                  Amenity,
                  PlaceAmenities,
                  Review,
                  ReviewUser,
                  ReviewPlace],
                 safe=True)
db.close()
