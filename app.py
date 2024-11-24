from flask import Flask, request, jsonify

app = Flask(__name__)

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

    def sort_songs(self):
        sortinglist = []
        current = self.head
        while current:
            sortinglist.append(current.song)
            current = current.next
        return sorted(sortinglist, key=lambda song: song.title)


playlists = {}



@app.route('/playlists', methods=['POST'])
def create_playlist():
    data = request.json
    name = data['name']
    if name in playlists:
        return jsonify({"error": "Playlist already exists"}), 400
    playlists[name] = Playlist(name)
    return jsonify({"message": f"Playlist '{name}' created successfully!"}), 201


@app.route('/playlists/<name>', methods=['DELETE'])
def delete_playlist(name):
    if name in playlists:
        del playlists[name]
        return jsonify({"message": f"Playlist '{name}' deleted successfully!"}), 200
    return jsonify({"error": "Playlist not found"}), 404


@app.route('/playlists/<name>/songs', methods=['POST'])
def add_song_to_playlist(name):
    if name not in playlists:
        return jsonify({"error": "Playlist not found"}), 404
    data = request.json
    playlist = playlists[name]
    playlist.add_song(data['id'], data['title'], data['artist'], data['duration'])
    return jsonify({"message": f"Song '{data['title']}' added to playlist '{name}'"}), 201


@app.route('/playlists/<name>/songs', methods=['GET'])
def get_songs_from_playlist(name):
    if name not in playlists:
        return jsonify({"error": "Playlist not found"}), 404
    playlist = playlists[name]
    songs = playlist.sort_songs()
    return jsonify([song.to_dict() for song in songs])


@app.route('/playlists/<name>/songs/<title>', methods=['DELETE'])
def delete_song_from_playlist(name, title):
    if name not in playlists:
        return jsonify({"error": "Playlist not found"}), 404
    playlist = playlists[name]
    response = playlist.delete_song(title)
    if response == "Song deleted":
        return jsonify({"message": f"Song '{title}' deleted from playlist '{name}'"}), 200
    return jsonify({"error": response}), 404


if __name__ == '__main__':
    # Seed Data
    playlists["Favorites"] = Playlist("Favorites")
    playlists["Favorites"].add_song(1, "Hello", "Adele", "3:05")
    playlists["Favorites"].add_song(2, "My Generation", "The Who", "2:05")
    playlists["Favorites"].add_song(3, "Crocodile Rock", "Elton John", "3:55")
    app.run(debug=True)
