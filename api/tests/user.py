"""
Unittest cases for the API routes to /users/*
"""
from base import BaseTestCase
from app.models.user import User
from data import users, user_without_email, user_dupl_email


class UserTestCase(BaseTestCase):
    table = [User]
    path = '/users'
    example = users[0]

    def test_create(self):
        count = 1
        for user in users:
            # It should create users with sequential ids.
            last_user = self.create_row(user, '201 CREATED')
            self.check(last_user.id, count)
            count += 1
        # It should return bad request when email is not given.
        last_user = self.create_row(user_without_email, '400 BAD REQUEST')
        self.check(last_user.email, 'rose@even.com')  # user not created
        # It should return code 10001 when trying to create user with
        # duplicated email
        last_user = self.check_dupl_entry(user_dupl_email, 10000)
        self.check(last_user.email, 'rose@even.com')

    def test_list(self):
        self.check_list()

    def test_get(self):
        self.check_get('User')

    def test_delete(self):
        self.check_delete('User')

    def test_update(self):
        upd_data = {'first_name': 'Philip', 'last_name': 'Even'}
        self.check_update(upd_data, 'User')
        # It should give internal server error when trying to change email
        resp = self.app.put('{}/{}'.format(self.path, 1),
                            data={'email': 'rose@gmail.com'})
        self.check(resp.status_code, 403)
