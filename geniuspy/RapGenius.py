import pprint
import requests

from geniuspy import __version__


pp = pprint.PrettyPrinter(indent=4)


class Error(Exception):
    pass


class NotFoundError(Error):
    pass


class Client:
    BASE_URL = 'https://api.rapgenius.com/'
    HEADERS = {
        'Accept': ['application/json'],
        'Content-Type': 'application/json',
        'User-Agent': "genius.py v%s" % __version__
    }

    @staticmethod
    def get(url, params=None):
        if params is None:
            params = {}
        response = requests.get(Client.BASE_URL+url, params=params, headers=Client.HEADERS)

        if response.status_code != 200:
            if response.status_code == 404:
                raise NotFoundError()
            else:
                raise Error("Received a %d HTTP response" % response.status_code)

        return response.json()

    # Descriptions are formatted in an irritating way, encapsulating the
    # various kinds of HTML tag that can be included. This parses that
    # into text, but some content may be lost.
    @staticmethod
    def parse_description(node):
        if type(node) is str or type(node) is unicode:
            return node
        elif type(node) == list:
            node = map(Client.parse_description, node)
            return ''.join(node)
        elif type(node) == dict and 'children' in node:
            return Client.parse_description(node["children"])
        else:
            return ''


class Artist:
    @staticmethod
    def find(artist_id):
        return Artist(artist_id)

    def __init__(self, artist_id=None, retrieve_info=True):
        self.id = artist_id
        self.document = None
        self.user = None
        self.name = None
        self.url = None
        #self.tracking_paths = None
        #self.description = None
        self.image_url = None
        # some currently unimplemented values from the API
        # 1. tracking_paths
        # 2. description
        if retrieve_info:
            self.retrieve_info()

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def retrieve_info(self, force=True):
        if self.document is None or force is True:
            self.document = Client.get("artists/%d" % self.id)
            self.user = self.document["response"]["artist"]["user"]
            self.name = self.document["response"]["artist"]["name"]
            self.url = self.document["response"]["artist"]["url"]
            self.image_url = self.document["response"]["artist"]["image_url"]
        return self

    def response(self):
        return self.document["response"]["artist"]

    # You seem to be able to load 25 songs at a time for an artist. I haven't
    # found a way to vary the number you get back from the query, but you can
    # paginate through in blocks of 25 songs.
    def songs(self, page=1):
        songs_url = "/artists/%d/songs/?page=%d" % (self.id, page)

        response_songs = Client.get(songs_url)["response"]["songs"]
        all_songs = []
        for response in response_songs:
            # if response["primary_artist"]["id"] == self.id:
            #     print("Using current artist")
            #     song_artist = self
            # else:
            #     print("Artist doesn't match, retrieving info")
            #     song_artist = Artist(response["primary_artist"]["id"])
            # print(u"[{}] ({})".format(song_artist.name, song_artist.id))
            song = Song(song_id=response["id"],
                        artist_id=response["primary_artist"]["id"],
                        title=response["title"],
                        retrieve_info=False
                        )
            all_songs.append(song)
        return all_songs


class Line:
    @staticmethod
    def find(line_id):
        return Line(line_id)

    def __init__(self, line_id=None, song=None, lyric=None):
        self.id = line_id
        self.song = song
        self.lyric = lyric
        self.response = None
        self.url = None
        if self.id:
            self.url = "referents/%d" % self.id


class Song:
    @staticmethod
    def find(song_id):
        return Song(song_id)

    def __init__(self, song_id=None, title=None, artist_id=None, retrieve_info=False):
        self.id = song_id
        self.title = title
        self.primary_artist_id = artist_id
        self.primary_artist = None
        self.document = None
        self.featured_artists = None
        self.producer_artists = None
        self.lyrics = None
        #self.tracking_paths = None
        # self.description = None
        # self.image_url = None
        # some currently unimplemented values from the API
        # 1. tracking_paths
        # 2. description
        if retrieve_info:
            self.retrieve_info()

    def retrieve_info(self, force=False):
        if self.document is None or force is True:
            self.document = Client.get("songs/%d" % self.id)
            self.primary_artist = Artist(artist_id=self.primary_artist_id)
            # pp.pprint(self.document)
            # parsed_lyrics = Song.parse_lines(self.document['response']['song']['lyrics']['dom']['children'])
            # print(parsed_lyrics)
            # self.user = self.document["response"]["artist"]["user"]
            # self.name = self.document["response"]["artist"]["name"]
            # self.url = self.document["response"]["artist"]["url"]
            # self.image_url = self.document["response"]["artist"]["image_url"]
        return self

    def get_lyrics(self, force=False):
        if self.lyrics is None or force:
            self.lyrics = Song.parse_lines(self.document['response']['song']['lyrics']['dom']['children'])
        return self.lyrics

    @staticmethod
    def parse_lines(node):
        # print("############## START parse_lines() ################")
        # if type(node) is str or type(node) is unicode:
        #     print("Valid String!")
        # pp.pprint(node)
        # print(type(node) == dict)
        # print('children' in node)

        if type(node) == list:
            node = map(Song.parse_lines, node)
            # print(node)
            return ''.join(node)
        elif type(node) == dict and 'children' in node:
            return Song.parse_lines(node["children"])
        elif type(node) == dict and 'tag' in node and node['tag'] == u'br':
            return u'\n'
        elif type(node) is str or type(node) is unicode:
            return node
        else:
            print("Unaccounted Type!")
            print(node)
            print(type(node))
            return

        # if type(node) is str or type(node) is unicode:
        #     return node
        # elif type(node) == list:
        #     node = map(Client.parse_description, node)
        #     return ''.join(node)
        # elif type(node) == dict and 'children' in node:
        #     return Client.parse_description(node["children"])
        # else:
        #     return ''