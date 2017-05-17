"""
Manage the API routes to /places/*<place_id>/books/*<book_id>
"""
from app.models.place_book import PlaceBook
from app.models.place import Place
from app.models.user import User
from flask_json import as_json, request
from app import app
from datetime import datetime, timedelta
import json
from return_styles import ListStyle


@app.route('/places/<place_id>/books', methods=['GET'])
@as_json
def get_place_bookings(place_id):
    """
    Get all bookings with id as place_id
    """
    data = PlaceBook.select().where(PlaceBook.place == place_id)
    return ListStyle.list(data, request), 200


@app.route('/places/<place_id>/books', methods=['POST'])
@as_json
def book_date(place_id):
    """
    Create a booking with id as place_id
    """
    data = request.form
    try:
        if 'user_id' not in data:
            raise KeyError('user_id')
        elif 'date_start' not in data:
            raise KeyError('date_start')
        book_start = datetime.strptime(
            data['date_start'], "%Y/%m/%d %H:%M:%S").replace(hour=0, minute=0, second=0)
        book_end = book_start + timedelta(days=int(data['number_nights']))
        bookings = PlaceBook.select().where(PlaceBook.place == place_id)
        for booking in bookings:
            date_start = booking.date_start.replace(hour=0, minute=0, second=0)
            date_end = date_start + timedelta(days=int(booking.number_nights))
            if book_start >= date_start and book_start < date_end:
                raise ValueError('booked')
            elif book_end > date_start and book_end <= date_end:
                raise ValueError('booked')
            elif date_start >= book_start and date_start < book_end:
                raise ValueError('booked')

        new = PlaceBook.create(
            place=place_id,
            user=data['user_id'],
            is_validated=data['is_validated'],
            date_start=datetime.strptime(
                data['date_start'], "%Y/%m/%d %H:%M:%S"),
            number_nights=data['number_nights']
        )
        res = {}
        res['code'] = 201
        res['msg'] = "Booking was created successfully"
        return res, 201
    except KeyError as e:
        res = {}
        res['code'] = 40000
        res['msg'] = 'Missing parameters'
        return res, 400
    except ValueError as e:
        if e.message == 'booked':
            res = {}
            res['code'] = 110000
            res['msg'] = 'Place unavailable at this date'
            return res, 410
    except Exception as error:
        res = {}
        res['code'] = 403
        res['msg'] = str(error)
        return res, 403


@app.route('/places/<place_id>/books/<book_id>', methods=['GET'])
@as_json
def get_booking(place_id, book_id):
    """
    Get a booking with id as place_id
    """
    try:
        booking = PlaceBook.get(PlaceBook.id == book_id)
    except Exception:
        return {'code': 404, 'msg': 'Booking not found'}, 404
    return booking.to_dict(), 200


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
        res['msg'] = "Booking was updated successfully"
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
        return {'code': 404, 'msg': 'Booking not found'}, 404
    booking = PlaceBook.delete().where(PlaceBook.id == book_id)
    booking.execute()
    response = {}
    response['code'] = 200
    response['msg'] = "Booking was deleted successfully"
    return response, 200
