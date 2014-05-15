from geniuspy import Client


class Artist:
    @staticmethod
    def find(artist_id):
        found = Artist(artist_id)
        return found.document

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

    def __getattr__(self, name):
        if self.document is None:
            self.retrieve_info()
        if name == 'name':
            return self.name
        elif name == 'image':
            return self.image_url
        elif name == 'url':
            return self.url
        #elif name == 'description':
        #    self.description = ''.join(map(Client.parse_description,
        #                                   self.document["response"]["artist"]["description"]["dom"]["children"]))
        #    return self.description

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
        for song in response_songs:
            song = Song(artist=Artist(name=song["primary_artist"]["name"],
                                      artist_id=song["primary_artist"]["id"],
                                      type='primary'),
                        title=song["title"],
                        id=song["id"])
        return response_songs

