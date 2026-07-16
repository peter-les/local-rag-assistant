#text_cleaner.py
import re


def clean_text(text):
    """
    Vyčistí text načítaný z PDF.
    """

    # Windows riadky
    text = text.replace("\r", "")

    # zjednotenie medzier
    text = re.sub(r"[ \t]+", " ", text)

    # tri a viac prázdnych riadkov -> dva
    text = re.sub(r"\n{3,}", "\n\n", text)

    # odstránenie medzier okolo nových riadkov
    text = re.sub(r" *\n *", "\n", text)

    # odstránenie medzier na začiatku a konci
    text = text.strip()

    return text