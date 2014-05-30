import unittest
from geniuspy import *


class TestArtist(unittest.TestCase):
    def setUp(self):
        self.artist = Artist(130)

    def test_url(self):
        self.assertEqual(self.artist.url, 'http://rapgenius.com/artists/Drake')

    def test_name(self):
        self.assertEqual(self.artist.name, 'Drake')

    def test_image(self):
        self.assertEqual(self.artist.image_url,
                         'http://images.rapgenius.com/a4a9dec18e3c348f0a13422ca9bda543.449x575x1.jpg')

    def test_description(self):
        self.assertTrue('Drake is part of a generation of new rappers' in self.artist.description)
