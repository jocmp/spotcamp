import re
from spotcamp.bandcamp import parser
from bs4 import BeautifulSoup


def test_search_results():
    html_body = open('./tests/fixtures/searchresult_track.html', 'r').read()
    soup = BeautifulSoup(html_body, 'html.parser')

    results = parser.parse_body(soup=soup)

    assert len(results) == 1
    result = results[0]

    assert result.art_url == 'https://f4.bcbits.com/img/a1308614804_7.jpg'
    assert result.heading == "19 (Payfone Extended Remix)"
    assert result.sub_heading == "from 19 by Piem & ANNNA"
    assert result.released == "released 16 July 2021"
    assert result.item_url == "https://dftd.bandcamp.com/track/19-payfone-extended-remix?from=search&search_item_id=1421311934&search_item_type=t&search_match_part=%3F&search_page_id=2077837144&search_page_no=1&search_rank=1&search_sig=c116717861304e85593eece2955c56ab"
    assert result.item_type == "TRACK"
