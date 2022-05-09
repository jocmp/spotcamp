from spotcamp import link_parser


def test_valid_link():
    spotify_resources = ['track', 'album', 'artist']
    for resource_type in spotify_resources:
        url = f'https://open.spotify.com/{resource_type}/1234'
        resource = link_parser.parse(url=url)
        assert resource.is_valid()


def test_invalid_resource():
    resource_type = 'bogus'
    url = f'https://open.spotify.com/{resource_type}/1234'  
    resource = link_parser.parse(url=url)
    assert not resource.is_valid()


def test_bad_path_segment_length():
    url = "https://open.spotify.com/wrong"
    resource = link_parser.parse(url=url)
    assert not resource.is_valid()


def test_bad_hostname():
    url = "https://www.example.com/shortcuts/abcdefg4444"
    resource = link_parser.parse(url=url)
    assert not resource.is_valid()
