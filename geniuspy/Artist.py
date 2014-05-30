from geniuspy.Client import Client
from geniuspy.Song import Song

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
            self.description = ''.join(map(Client.parse_description,
                                           self.document["response"]["artist"]["description"]["dom"]["children"]))
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