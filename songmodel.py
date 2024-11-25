class Song:
    def __init__(self, id, title, artist, duration):
        self.id = id
        self.title = title
        self.artist = artist
        self.duration = duration

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "artist": self.artist,
            "duration": self.duration
        }

class Node:
    def __init__(self, song):
        self.song = song
        self.prev = None
        self.next = None