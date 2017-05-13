#!/usr/bin/python3
import os
ENV = os.environ.get('AIRBNB_ENV')

if ENV == 'production':
    DEBUG = False
    HOST = "0.0.0.0"
    PORT = 3000
    DATABASE = {
        'host': "158.69.91.91",
        'user': 'airbnb_user_prod',
        'database': 'airbnb_prod',
        'port': 3333,
        'charset': 'utf8',
        'password': os.environ.get('AIRBNB_DATABASE_PWD_PROD')
    }
elif ENV == 'development':
    DEBUG = False
    HOST = localhost
    PORT = 3333
    DATABASE = {
        'host': "158.69.91.91",
        'user': 'airbnb_user_dev',
        'database': 'airbnb_dev',
        'port': 3000,
        'charset': 'utf8',
        'password': os.environ.get('AIRBNB_DATABASE_PWD_DEV')
    }

print(DATABASE)
