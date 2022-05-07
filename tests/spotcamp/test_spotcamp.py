from urllib import parse
from spotcamp import spotcamp
from spotcamp.responses import Status


def test_find_artist_when_query_is_empty(mocker):
    spotify = mocker.Mock()
    query = ''
    response = spotcamp.find(query=query, spotify=spotify)
    assert spotify.artist.call_count == 0
    assert response.is_failure()


def test_find_artist_when_query_url_is_present(mocker):
    spotify = mocker.Mock()
    artist_id = '6kBDZFXuLrZgHnvmPu9NsG'
    result_artist_name = 'Aphex Twin'
    query = f'https://open.spotify.com/artist/{artist_id}?si=HHxli1A0Qk2AFEp1OkVXgQ'
    bandcamp_query = parse.quote(result_artist_name)
    spotify.artist.return_value = {'name': result_artist_name}

    response = spotcamp.find(query=query, spotify=spotify)

    spotify.artist.assert_called_with(artist_id=artist_id)
    assert response.status == Status.SUCCESS
    assert response.value == f'https://bandcamp.com/search?item_type=b&q={bandcamp_query}'


def test_find_song_with_artist(mocker):
    spotify = mocker.Mock()
    track_id = '1beOhReE4hMg0ti0181AcU'
    result_track_name = 'All I See'
    query = f'https://open.spotify.com/track/{track_id}?si=3f3e15dbecac473d'
    bandcamp_query = parse.quote(result_track_name)
    spotify.track.return_value = {
        'name': result_track_name
    }

    response = spotcamp.find(query=query, spotify=spotify)

    spotify.track.assert_called_with(track_id=track_id)
    assert response.status == Status.SUCCESS
    assert response.value == f'https://bandcamp.com/search?item_type=t&q={bandcamp_query}'
