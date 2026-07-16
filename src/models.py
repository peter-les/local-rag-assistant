from dataclasses import dataclass


@dataclass
class Document:

    author: str

    book: str

    page: int

    text: str
	
@dataclass
class SearchResult:

    author: str

    book: str

    page: int

    text: str

    distance: float