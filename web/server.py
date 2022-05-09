from flask import Flask, redirect, render_template, request
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotcamp import spotcamp

app = Flask(__name__)

spotify = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials())


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/spotcamp')
def get_spotcamp():
    query = request.args.get('q')
    response = spotcamp.find(spotify=spotify, query=query)

    if response.is_failure():
        return redirect('/', code=302)

    response_value = response.value
    return render_template(
        'spotcamp.html',
        search_url=response_value['search_url'],
        resource_type=response_value['resource_type'],
        item_name=response_value['item_name'],
        search_results=response_value['search_results']
    )
