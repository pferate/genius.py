from geniuspy.rapgenius.client import Client

class Artist:
    @staticmethod
    def find(id):
        found = Artist(id)
        return found.document

    def __init__(self, id, **kwargs):
        self.id = id
        if 'name' in kwargs:
            self.name = kwargs['name']
        if 'type' in kwargs:
            self.type = kwargs['type']
        self.document = Client.get("artists/%d" % id)

    def __getattr__(self, name):
        if name == 'name':
            return self.document["response"]["artist"]["name"]
        elif name == 'image':
            return self.document["response"]["artist"]["image_url"]
        elif name == 'url':
            return self.document["response"]["artist"]["url"]
        elif name == 'description':
            self.description = ''.join(map(Client.parse_description, self.document["response"]["artist"]["description"]["dom"]["children"]))
            return self.description
        elif name == 'songs':
            return self.__songs()

    def response(self):
        return self.document["response"]["artist"]

    # You seem to be able to load 25 songs at a time for an artist. I haven't
    # found a way to vary the number you get back from the query, but you can
    # paginate through in blocks of 25 songs.
    def __songs(self, options = {'page': 1}):
        songs_url = "/artists/%d/songs/?page=%d" % (self.id, options["page"])

        response_songs = Client.get(songs_url)["response"]["songs"]
        for song in response_songs:
            song = Song(artist=Artist(name=song["primary_artist"]["name"], id=song["primary_artist"]["id"], type='primary'), title=song["title"], id=song["id"])
        return response_songs

