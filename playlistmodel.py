from songmodel import Song, Node

class Playlist:
    def __init__(self, name):
        self.name = name
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
            if current.song.title == title:
                if current == self.head:
                    self.head = current.next
                if current == self.tail:
                    self.tail = current.prev
                if current.prev:
                    current.prev.next = current.next
                if current.next:
                    current.next.prev = current.prev
                return "Song deleted"
            current = current.next
        return "Song not found"

    def get_song(self, title):
        current = self.head
        while current:
            if current.song.title == title:
                return current.song.to_dict()
            current = current.next
        return None

    def get_song2(self, title):
        current = self.head
        while current:
            if current.song.title == title:
                return current.song
            current = current.next
        return None

    def sort_songs(self):
        sortinglist = []
        current = self.head
        while current:
            sortinglist.append(current.song)
            current = current.next
        return sorted(sortinglist, key=lambda song: song.title)