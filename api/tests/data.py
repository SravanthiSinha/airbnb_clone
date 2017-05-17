from datetime import datetime, timedelta

users = [
    {'first_name': 'Sravanthi', 'last_name': 'sinha',
     'email': 'sravanthi.sinha@holbertonschool.com',
     'password': '987654', 'is_admin': True},
    {'first_name': 'Rose', 'last_name': 'Even',
     'email': 'rose@even.com', 'password': '123456',
     'is_admin': False}]

user_without_email = {'first_name': 'Jony', 'last_name': 'Snow',
                      'password': '32145', 'is_admin': False}
user_dupl_email = {'first_name': 'rose', 'last_name': 'Even',
                   'email': 'rose@even.com',
                   'password': '654', 'is_admin': True}

states = [{'name': 'California'}, {'name': 'Utah'},
          {'name': 'Texas'}, {'name': 'Alaska'}]
cities = [{'name': 'Los Angeles'},
          {'name': 'San jose'},
          {'name': 'San Francisco'}]
places = [{'name': 'Boba Pod',
           'owner_id': 1,
           'city_id': 3,
           'description': "welcome",
           'number_rooms': 4,
           'number_bathrooms': 2,
           'max_guest': 2,
           'price_by_night': 60,
           'latitude': 24.77,
           'longitude': 102.41},
          {'name': 'Honey Pod',
           'owner_id': 1,
           'city_id': 3,
           'description': "welcome",
           'number_rooms': 4,
           'number_bathrooms': 2,
           'max_guest': 5,
           'price_by_night': 60,
           'latitude': 38.87,
           'longitude': 92.31}]

place_br = {
    'name': 'Boba Pod',
    'city_id': 3,
    'description': "welcome",
    'number_rooms': 4,
    'number_bathrooms': 2,
    'latitute': 97.97,
    'longitude': 128.41}

dupl_place = {
    'name': 'Boba Pod',
    'owner_id': 1,
    'city_id': 1,
    'description': "welcome",
    'number_rooms': 4,
    'number_bathrooms': 2,
    'max_guest': 2,
    'price_by_night': 60,
    'latitude': 24.77,
    'longitude': 102.41}

pbooks = [{'user_id': 2,
           'date_start': datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
           'number_nights': 2,
           'is_validated': False,
           },
          {'user_id': 1,
           'date_start': (datetime.now() + timedelta(days=6)).strftime("%Y/%m/%d %H:%M:%S"),
           'number_nights': 7,
           'is_validated': True,
           }]

pb_br = {'user': 1, 'number_nights': 4}

amenities = [{'name': 'Wifi'},
             {'name': 'Room Service'},
             {'name': 'Dinner'},
             {'name': 'Breakfast'}]

reviews = [
    {'message': 'First review: First review', 'stars': 5, 'user_id': 2},
    {'message': 'Second review: Second review', 'stars': 3, 'user_id': 2},
    {'message': 'Third review: Third review', 'stars': 2, 'user_id': 2}
]
