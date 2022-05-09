
from dataclasses import dataclass
from urllib.parse import urlsplit
from spotcamp import spotify_resource_types


def parse(url):
    if not url:
        return SpotifyResource()

    result = urlsplit(url)
    if not result.hostname == 'open.spotify.com':
        return SpotifyResource()

    segments = [
        s for s in result.path.split('/') if len(s) > 0
    ]

    if not len(segments) == 2:
        return SpotifyResource()

    (resource_type, resource_id) = segments

    if resource_type not in spotify_resource_types.ALL:
      return SpotifyResource()

    return SpotifyResource(
        resource_type=resource_type,
        resource_id=resource_id
    )


@dataclass
class SpotifyResource():
    resource_type: str = ''
    resource_id: str = ''

    def is_valid(self):
        return bool(self.resource_type) and bool(self.resource_id)
