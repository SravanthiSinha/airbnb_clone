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
           'owner': 1,
           'city': 3,
           'description': "welcome",
           'number_rooms': 4,
           'number_bathrooms': 2,
           'max_guest': 2,
           'price_by_night': 60,
           'latitude': 24.77,
           'longitude': 102.41},
          {'name': 'Honey Pod',
           'owner': 1,
           'city': 3,
           'description': "welcome",
           'number_rooms': 4,
           'number_bathrooms': 2,
           'max_guest': 5,
           'price_by_night': 60,
           'latitude': 38.87,
           'longitude': 92.31}]

place_br = {
    'name': 'Boba Pod',
    'owner': 2,
    'city': 3,
    'description': "welcome",
    'number_rooms': 4,
    'number_bathrooms': 2,
    'max_guest': 4,
    'latitute': 97.97,
    'longitude': 128.41}

dupl_place = {
    'name': 'Boba Pod',
    'owner': 1,
    'city': 1,
    'description': "welcome",
    'number_rooms': 4,
    'number_bathrooms': 2,
    'max_guest': 2,
    'price_by_night': 60,
    'latitude': 24.77,
    'longitude': 102.41}

pbooks = [{'place': 1,
           'user': 2,
           'date_start': '2017/05/21 09:00:00',
           'number_nights': 17,
           'is_validated': False, },
          {'place': 2,
           'user': 2,
           'date_start': '2017/05/20 08:00:00',
           'number_nights': 7,
           'is_validated': True,
           }]

pb_br = {'place': 1, 'user': 1, 'number_nights': 4}

amenities = [{'name': 'Wifi'},
             {'name': 'Room Service'},
             {'name': 'Dinner'},
             {'name': 'Breakfast'}]
