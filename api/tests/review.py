from base import BaseTestCase
from app.models.review import Review
from app.models.review_user import ReviewUser
from app.models.user import User
from data import *


class ReviewTestCase(BaseTestCase):
    table = [User, Review, ReviewUser]
    path = '/users/1/reviews'
    example = reviews[0]

    def test_create(self):
        self.create_users()
        count = 1
        for review in reviews:
            last_review = self.create_row(review, '201 CREATED')
            self.check(last_review.id, count)
            count += 1
        # It should return 404 if user_id is not found(GET)
        review_table = {'model': Review, 'path': '/users/50/reviews'}
        resp = self.app.get('/users/50/review', reviews[0])
        self.check(resp.status_code, 404)
        # It should return 404 if user_id is not found(POST)
        review_table = {'model': Review, 'path': '/users/50/reviews'}
        resp = self.app.post('/users/50/review', reviews[0])
        self.check(resp.status_code, 404)

    def test_list(self):
        self.create_users()
        self.check_list()

    def test_get(self):
        self.create_users()
        self.check_get('Review')

    def test_delete(self):
        self.create_users()
        self.check_delete('Review')
