from flask import Flask, render_template, request
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


app = Flask(__name__)

spotify = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials())


@app.route('/')
def index():
    query = request.args.get('q')
    results = find_results(query=query)
    return render_template('index.html', results=results)


def find_results(query):
    if not query:
        return []

    results = spotify.search(q=query, type='artist')

    artists = results['artists']['items']

    while results['artists']['next']:
        results = spotify.next(results)
        artists.extend(results['artists']['items'])

    results = map(
        lambda a: f'{a["name"]} with a popularity of {a["popularity"]}', artists)

    return results
