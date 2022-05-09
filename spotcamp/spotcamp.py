import structlog
from typing import Any
from requests import Response
import spotipy
from urllib import parse
from spotcamp import link_parser
from spotcamp.responses import Response
from spotcamp.bandcamp import item_types, parser
import spotcamp.spotify_resource_types as spotify_resource_types


def find(spotify: spotipy.Spotify, query: str | None, parser: parser = parser) -> Response[dict[str, Any]]:
    spotify_resource = link_parser.parse(url=query)
    if not spotify_resource.is_valid():
        return Response.failure(value="Link format not recognized.")

    item_name = _find_name(spotify=spotify, spotify_resource=spotify_resource)
    bandcamp_query = _build_bandcamp_query(item_name=item_name)
    item_type = _spotify_to_bandcamp_item_type(
        spotify_resource=spotify_resource
    )

    try:
        search_url = f'https://bandcamp.com/search?item_type={item_type}&q={bandcamp_query}'

        results = parser.parse_page(url=search_url)

        response_value = {
            'search_url': search_url,
            'search_results': results,
            'resource_type': spotify_resource.resource_type,
            'item_name': item_name
        }
        return Response.success(value=response_value)
    except Exception as error:
        log_error(error, spotify_resource=spotify_resource)
        return Response.failure()


def _build_bandcamp_query(item_name):
    return parse.quote(item_name)


def _find_name(spotify: spotipy.Spotify, spotify_resource: link_parser.SpotifyResource):
    result = _find_resource(spotify=spotify, spotify_resource=spotify_resource)
    if not result:
        return None

    return result['name']


def _find_resource(spotify: spotipy.Spotify, spotify_resource: link_parser.SpotifyResource):
    match spotify_resource.resource_type:
        case spotify_resource_types.ARTIST:
            return spotify.artist(artist_id=spotify_resource.resource_id)
        case spotify_resource_types.TRACK:
            return spotify.track(track_id=spotify_resource.resource_id)
        case spotify_resource_types.ALBUM:
            return spotify.album(album_id=spotify_resource.resource_id)

    return None


def _spotify_to_bandcamp_item_type(spotify_resource: link_parser.SpotifyResource) -> str:
    match spotify_resource.resource_type:
        case spotify_resource_types.ARTIST:
            return item_types.ARTISTS_AND_LABELS
        case spotify_resource_types.TRACK:
            return item_types.TRACK
        case spotify_resource_types.ALBUM:
            return item_types.ALBUM


def log_error(error, spotify_resource):
    structlog.get_logger().error(
        'spotcamp.find.error',
        resource_type=spotify_resource.resource_type,
        resource_id=spotify_resource.resource_id,
        error_class_name=error.__class__.__name__
    )
