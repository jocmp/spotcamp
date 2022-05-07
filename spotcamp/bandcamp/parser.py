import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
from bs4.element import Tag
from spotcamp.bandcamp.search_result import SearchResult


def parse_page(url) -> list[SearchResult]:
    with urlopen(url) as response:
        body = response.read()
    soup = BeautifulSoup(body, 'html.parser')
    return parse_body(soup=soup)


def parse_body(soup: BeautifulSoup):
    results = map(_build_search_result, soup.find_all(class_='searchresult'))
    return list(results)


def _build_search_result(tag: Tag) -> SearchResult:
    art_url = tag.find(class_='art').find('img').attrs['src']
    heading = _clean_text(tag.find(class_='heading').get_text())
    sub_heading = _clean_text(tag.find(class_='subhead').get_text())
    released = _clean_text(tag.find(class_='released').get_text())
    item_url = tag.find(class_='itemurl').find('a').attrs['href']
    item_type = _clean_text(tag.find(class_='itemtype').get_text())

    return SearchResult(
        art_url=art_url,
        heading=heading,
        sub_heading=sub_heading,
        released=released,
        item_url=item_url,
        item_type=item_type
    )


def _clean_text(text):
    if not text:
        return ''
    cleaned = text.replace('\n', ' ').strip()
    return re.sub(r"\s\s+", " ", cleaned)
