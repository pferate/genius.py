import unittest
from geniuspy.rapgenius.client import Client
from geniuspy.rapgenius.exceptions import NotFoundError

class TestClient(unittest.TestCase):
    def test_failed_request(self):
        self.assertRaises(NotFoundError, Client.get, 'foobar/123')
