"""
Manage the API routes to /places/*<place_id>/books/*<book_id>
"""
from app.models.place_book import PlaceBook
from app.models.place import Place
from app.models.user import User
from flask_json import as_json, request
from app import app
from datetime import datetime
import json


@app.route('/places/<place_id>/books', methods=['GET'])
@as_json
def get_place_bookings(place_id):
    """
    Get all bookings with id as place_id
    """
    booked_dates = []
    data = PlaceBook.select().where(PlaceBook.place == place_id)
    for row in data:
        booked_dates.append(row.to_hash())
    return {"result": booked_dates}, 200


@app.route('/places/<place_id>/books', methods=['POST'])
@as_json
def book_date(place_id):
    """
    Create a booking with id as place_id
    """
    data = request.form
    new = PlaceBook.create(
        place=place_id,
        user=data['user_id'],
        is_validated=data['is_validated'],
        date_start=datetime.strptime(data['date_start'], "%Y/%m/%d %H:%M:%S"),
        number_nights=data['number_nights']
    )
    res = {}
    res['code'] = 201
    res['msg'] = "Booking of place was created successfully"
    return res, 201


@app.route('/places/<place_id>/books/<book_id>', methods=['GET'])
@as_json
def get_booking(place_id, book_id):
    """
    Get a booking with id as place_id
    """
    try:
        booking = PlaceBook.get(PlaceBook.id == book_id)
    except Exception:
        return {'code': 404, 'msg': 'Book not found'}, 404
    return booking.to_hash(), 200


@app.route('/places/<place_id>/books/<book_id>', methods=['PUT'])
@as_json
def update_booking(place_id, book_id):
    """
    Update the booking details of booking with id as place_id
    """
    try:
        booking = PlaceBook.get(PlaceBook.id == book_id)
        data = request.form
        for key in data:
            if key == 'user_id':
                raise Exception('User cannot be changed')
            elif key == 'is_validated':
                booking.is_validated = data[key]
            elif key == 'date_start':
                booking.date_start = datetime.strptime(
                    data[key], "%Y/%m/%d %H:%M:%S")
            elif key == 'number_nights':
                booking.number_nights = data[key]
        booking.save()
        res = {}
        res['code'] = 200
        res['msg'] = "Booking of place was updated successfully"
        return res, 200
    except Exception as error:
        res = {}
        res['code'] = 403
        res['msg'] = str(error)
        return res, 403


@app.route('/places/<place_id>/books/<book_id>', methods=['DELETE'])
@as_json
def delete_booking(place_id, book_id):
    """
    Delete booking with id as place_id
    """
    try:
        booking = PlaceBook.get(PlaceBook.id == book_id)
    except Exception:
        return {'code': 404, 'msg': 'Book not found'}, 404
    booking = PlaceBook.delete().where(PlaceBook.id == book_id)
    booking.execute()
    response = {}
    response['code'] = 200
    response['msg'] = "Booking was deleted"
    return response, 200
