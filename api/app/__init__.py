from flask import Flask
from flask_json import FlaskJSON

'''initialized Flask application'''
app = Flask(__name__)

app.config['JSON_ADD_STATUS'] = False

'''initialized FlaskJSON with app'''
json = FlaskJSON(app)

'''Imports all views'''
from views import *
