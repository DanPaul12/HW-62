class Song:
    def __init__(self, id, title, artist, duration):
        self.id = id
        self.title = title
        self.artist = artist
        self.duration = duration

class Node:
    def __init__(self, song):
        self.song = song
        self.prev = None
        self.next = None

class Playlist:
    def __init__(self):
        self.head = None
        self.tail = None

    def add_song(self, id, title, artist, duration):
        new_song = Song(id, title, artist, duration)
        new_node = Node(new_song)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

    def delete_song(self, title):
        current = self.head
        while current:
            if current.title == title:
                if current == self.head:
                    self.head.next = self.head
                if current == self.tail:
                    self.tail.prev = self.tail
                if current.prev:
                    current.prev.next = current
                if current.next:
                    current.next.prev = current.prev
                return "song deleted"
            current = current.next
        return "song not deleted"
