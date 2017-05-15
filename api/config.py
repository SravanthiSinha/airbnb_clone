import os

ENV = os.environ.get('AIRBNB_ENV')
DATABASE ={}
DATABASE['charset'] = 'utf8'
DATABASE['host'] = "158.69.91.91"

if ENV == 'production':
    DEBUG = False
    HOST = "0.0.0.0"
    PORT = 3000
    DATABASE['user'] = 'airbnb_user_prod'
    DATABASE['database'] = 'airbnb_prod'
    DATABASE['port'] = 3306
    DATABASE['password'] = os.environ.get('AIRBNB_DATABASE_PWD_PROD')
elif ENV == 'development':
    DEBUG = True
    HOST = 'localhost'
    PORT = 3333
    DATABASE['user'] = 'airbnb_user_dev'
    DATABASE['database'] = 'airbnb_dev'
    DATABASE['port'] = 3306
    DATABASE['password'] = os.environ.get('AIRBNB_DATABASE_PWD_DEV')
