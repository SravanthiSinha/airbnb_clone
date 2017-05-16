from app import app
import unittest
from datetime import datetime
import json


class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_200(self):
        rv = self.app.get('/')
        self.assertEqual(rv.status_code, 200)

    def test_status(self):
        rv = self.app.get('/')
        status = json.loads(rv.data)['status']
        self.assertEqual(status, 'OK')

    def test_time(self):
        rv = self.app.get('/')
        time = str(json.loads(rv.data)['time'])
        time_compare = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        self.assertEqual(time, time_compare)

    def test_time_utc(self):
        rv = self.app.get('/')
        utc_time = str(json.loads(rv.data)['utc_time'])
        utc_time_compare = datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S")
        self.assertEqual(utc_time, utc_time_compare)


if __name__ == '__main__':
    unittest.main()
