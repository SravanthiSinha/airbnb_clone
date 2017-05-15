from app.models.base import *
from app.models.user import *
from app.models.state import *
from app.models.city import *
from app.models.place import *
from app.models.place_book import *
from app.models.amenity import *
from app.models.place_amenity import *

BaseModel.database.init(DATABASE['database'])
BaseModel.database.connect()
BaseModel.database.create_tables([User, State, City, Place, PlaceBook, Amenity, PlaceAmenities], safe=True)
