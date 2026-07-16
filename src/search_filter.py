from dataclasses import dataclass


@dataclass
class SearchFilter:
    """
    Určuje, v ktorých dokumentoch sa má vyhľadávať.
    None = bez obmedzenia.
    """

    authors: list[str] | None = None

    books: list[str] | None = None

    top_k: int | None = None