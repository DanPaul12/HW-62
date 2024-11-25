from flask import Flask, request, jsonify
from playlistmodel import Playlist

app = Flask(__name__)

playlists = {}

#Routes-------------------------------------------------------------------------------

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

@app.route('/playlists/<name>/songs/<title>', methods=['PUT'])
def update_song_in_playlist(name, title):
    if name not in playlists:
        return jsonify({"error": "Playlist not found"}), 404
    playlist = playlists[name]
    song = playlist.get_song2(title)
    if song:
        data = request.json
        song.id= data['id']
        song.title =data['title']
        song.artist =data['artist']
        song.duration =data['duration']
        return jsonify({"message":"song updated"}), 200
    else:
        return jsonify({"message":"song updated"}), 404



if __name__ == '__main__':
    playlists["Favorites"] = Playlist("Favorites")
    playlists["Favorites"].add_song(1, "Hello", "Adele", "3:05")
    playlists["Favorites"].add_song(2, "My Generation", "The Who", "2:05")
    playlists["Favorites"].add_song(3, "Crocodile Rock", "Elton John", "3:55")
    app.run(debug=True)
