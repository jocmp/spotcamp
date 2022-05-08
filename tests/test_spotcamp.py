from app.spotcamp import spotcamp
from app.spotcamp.responses import Status


def test_find_artist_when_query_is_empty(mocker):
    spotify = mocker.Mock()
    query = ''
    response = spotcamp.find_artists(query=query, spotify=spotify)
    assert spotify.artist.call_count == 0
    assert response.is_failure()


def test_find_artist_when_query_url_is_present(mocker):
    spotify = mocker.Mock()
    artist_id = '6kBDZFXuLrZgHnvmPu9NsG'
    result_artist_name = 'Aphex Twin'
    query = f'https://open.spotify.com/artist/{artist_id}?si=HHxli1A0Qk2AFEp1OkVXgQ'
    spotify.artist.return_value = {'name': result_artist_name}
    response = spotcamp.find_artists(query=query, spotify=spotify)
    spotify.artist.assert_called_with(artist_id=artist_id)
    assert response.status == Status.SUCCESS
    assert response.value == f'https://bandcamp.com/search?item_type=b&q={result_artist_name}'
