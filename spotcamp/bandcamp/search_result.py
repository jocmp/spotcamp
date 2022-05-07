from dataclasses import dataclass


@dataclass
class SearchResult():
    art_url: str = None
    heading: str = ''
    sub_heading: str = ''
    item_type: str = ''
    item_url: str = None
    released: str = ''
