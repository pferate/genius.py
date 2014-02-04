import unittest
from geniuspy.rapgenius.artist import Artist

class TestArtist(unittest.TestCase):
    def setUp(self):
        self.artist = Artist(130)

    def test_url(self):
        self.assertEqual(self.artist.url, 'http://rapgenius.com/artists/Drake')

    def test_name(self):
        self.assertEqual(self.artist.name, 'Drake')

    def test_image(self):
        self.assertEqual(self.artist.image, 'http://images.rapgenius.com/2b3fa8326a5277fa31f2012a7b581e2e.500x319x11.gif')

    def test_description(self):
        self.assertTrue('Drake is part of a generation of new rappers' in self.artist.description)
