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