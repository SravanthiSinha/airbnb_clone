from flask_json import as_json
from datetime import datetime
from app.models.base import peewee_mysql_db as db
from app import app

'''allow only get request'''


@app.route("/", methods=['GET'])
@as_json
def index():
    data = {}
    data['status'] = 'OK'
    data['utc_time'] = datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S")
    data['time'] = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    return data


@app.before_request
def before_request():
    db.connect()


@app.after_request
def after_request(response):
    db.close()
    return response


@app.errorhandler(404)
@as_json
def not_found(e):
    ''' return a JSON with code = 404 and msg = "not found"'''
    return {"code": 404, "msg": "not found"}, 404
