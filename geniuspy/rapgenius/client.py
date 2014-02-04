import re
import requests

from geniuspy.rapgenius.meta import Meta
from geniuspy.rapgenius.exceptions import Error, NotFoundError

class Client:
    BASE_URL = 'https://api.rapgenius.com/'
    HEADERS = {
        'Accept': ['application/json'],
        'Content-Type': 'application/json',
        'User-Agent': "genius.py v%s" % Meta.VERSION
    }

    @staticmethod
    def get(url, params={}):
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
        if type(node) == str or type(node) == unicode:
            return node
        elif type(node) == list:
            node = map(Client.parse_description, node)
            return ''.join(node)
        elif type(node) == dict and 'children' in node:
            return Client.parse_description(node["children"])
        else:
            return ''
