from flask import Flask, redirect, render_template, request
import spotipy
import os
from urllib import parse
from spotipy.oauth2 import SpotifyClientCredentials


app = Flask(__name__)

spotify = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/spotcamp')
def spotcamp():
    query = request.args.get('q')
    if not query:
        return redirect('/', code=302)

    result = parse.urlsplit(query)
    (_, artist_id) = os.path.split(result.path)
    artist = spotify.artist(artist_id=artist_id)

    search_url = f'https://bandcamp.com/search?item_type=b&q={artist["name"]}'
    return redirect(search_url, code=302)
