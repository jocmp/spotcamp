from requests import Response
import spotipy
import os
from urllib import parse
from app.spotcamp.responses import Response


def find_artists(spotify: spotipy.Spotify, query: str | None) -> Response:
    if not query:
        return Response.failure()

    result = parse.urlsplit(query)
    (_, artist_id) = os.path.split(result.path)
    try:
        artist = spotify.artist(artist_id=artist_id)
        search_url = f'https://bandcamp.com/search?item_type=b&q={artist["name"]}'
        return Response.success(value=search_url)
    except:
        return Response.failure()
