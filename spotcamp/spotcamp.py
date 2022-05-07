from requests import Response
import spotipy
from urllib import parse
from spotcamp.bandcamp.search_result import SearchResult
from spotcamp.responses import Response
from spotcamp.bandcamp import item_types
import spotcamp.spotify_resource_types as spotify_resource_types


def find(spotify: spotipy.Spotify, query: str | None) -> Response[SearchResult]:
    if not query:
        return Response.failure()

    result = parse.urlsplit(query)
    (resource_type, resource_id) = [
        s for s in result.path.split('/') if len(s) > 0]
    bandcamp_query = _build_bandcamp_query(
        item_name=_find_name(
            spotify=spotify,
            resource_id=resource_id,
            resource_type=resource_type
        )
    )
    item_type = _spotify_to_bandcamp_item_type(resource_type)
    try:
        search_url = f'https://bandcamp.com/search?item_type={item_type}&q={bandcamp_query}'
        return Response[list[SearchResult]].success(value=search_url)
    except:
        return Response.failure()


def _build_bandcamp_query(item_name):
    return parse.quote(item_name)


def _find_name(spotify: spotipy.Spotify, resource_type: str, resource_id: str):
    result = _find_resource(
        spotify=spotify,
        resource_type=resource_type,
        resource_id=resource_id
    )
    if not result:
        return None

    return result['name']


def _find_resource(spotify: spotipy.Spotify, resource_type: str, resource_id: str):
    match resource_type:
        case spotify_resource_types.ARTIST:
            return spotify.artist(artist_id=resource_id)
        case spotify_resource_types.TRACK:
            return spotify.track(track_id=resource_id)
        case spotify_resource_types.ALBUM:
            return spotify.album(album_id=resource_id)

    return None


def _spotify_to_bandcamp_item_type(resource_type) -> str:
    match resource_type:
        case spotify_resource_types.ARTIST:
            return item_types.ARTISTS_AND_LABELS
        case spotify_resource_types.TRACK:
            return item_types.TRACK
        case spotify_resource_types.ALBUM:
            return item_types.ALBUM
