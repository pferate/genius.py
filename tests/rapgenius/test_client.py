import unittest
from geniuspy import Client
from geniuspy import NotFoundError


class TestClient(unittest.TestCase):
    def test_failed_request(self):
        self.assertRaises(NotFoundError, Client.get, 'foobar/123')
