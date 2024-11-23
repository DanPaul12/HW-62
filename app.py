from flask import Flask, request, jsonify

app = Flask(__name__)

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
            if current.song.title == title:
                if current == self.head:
                    self.head = current.next
                if current == self.tail:
                    self.tail = current.prev
                if current.prev:
                    current.prev.next = current.next
                if current.next:
                    current.next.prev = current.prev
                return "song deleted"
            current = current.next
        return "song not deleted"
    
    def get_song(self, title):
        current = self.head
        while current:
            if current.song.title == title:
                print(current.song.title + ' by ' + current.song.artist)
                return current.song
            current = current.next
        return "song not found"
    
    def sort_songs(self):
        sortinglist = []
        current = self.head
        while current:
            sortinglist.append(current.song)
            current = current.next
        newlist = sorted(sortinglist, key=lambda song: song.title)
        return newlist
        
    
playlist = Playlist()
playlist.add_song(1, "Hello", "Adele", "3:05")
playlist.add_song(2, "My Generation", "The Who", "2:05")
playlist.add_song(3, "Crocodile Rock", "Elton John", "3:55")
playlist.delete_song('My Generation')
playlist.get_song('Hello')
playlist.sort_songs()


@app.route('/songs/<title>', methods = ['GET'])
def getsong(title):
    song = playlist.get_song(title)
    return jsonify(song)

@app.route('/songs/<title>', methods = ['DELETE'])
def deletesong(title):
    song = playlist.delete_song(title)
    return jsonify('song deleted')

@app.route('/playlist', methods = ['GET'])
def getsongs():
    songs = playlist.sort_songs()
    for song in songs:
        return jsonify(song.title + " by " + song.artist)

@app.route('/addsong', methods= ['POST'])
def create_song():
    data = request.json
    playlist.add_song(data['id'], data['name'], data['artist'], data['duration'])
    return 'song added'
