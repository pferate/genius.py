from geniuspy.Artist import Artist
from geniuspy.Client import Client


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