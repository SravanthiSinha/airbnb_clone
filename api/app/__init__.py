from flask import Flask
from flask_json import FlaskJSON
from flask_cors import CORS, cross_origin

'''initialized Flask application'''
app = Flask(__name__)

CORS(app)

app.config['JSON_ADD_STATUS'] = False

'''initialized FlaskJSON with app'''
json = FlaskJSON(app)

'''Imports all views'''
from views import *
