#!/usr/bin/python3


peewee_mysql_db.connect()
peewee_mysql_db.create_tables([BaseModel,User,State,City,Place,PlaceBook,Amenity,PlaceAmenities],safe=True)
