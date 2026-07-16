#chunker.py
from models import Document
from config import CHUNK_SIZE_WORDS, CHUNK_OVERLAP_WORDS
import re


def split_into_paragraphs(text: str) -> list[str]:
    """
    Rozdelí text na odseky.
    """

    paragraphs = []

    for paragraph in text.split("\n\n"):

        paragraph = paragraph.strip()

        if paragraph:
            paragraphs.append(paragraph)

    return paragraphs


def split_large_paragraph(paragraph: str) -> list[str]:
    """
    Rozdelí dlhý odsek na chunky podľa počtu slov.
    """

    sentences = re.split(r'(?<=[.!?])\s+', paragraph)

    chunks = []

    current_words = []

    current_count = 0

    for sentence in sentences:

        words = sentence.split()

        if current_count + len(words) <= CHUNK_SIZE_WORDS:

            current_words.extend(words)

            current_count += len(words)

        else:

            if current_words:
                chunks.append(" ".join(current_words))

            current_words = words.copy()

            current_count = len(words)

    if current_words:
        chunks.append(" ".join(current_words))

    return chunks


def apply_overlap(chunks: list[str]) -> list[str]:
    """
    Pridá overlap medzi chunkami.
    """

    if len(chunks) <= 1:
        return chunks

    result = [chunks[0]]

    for chunk in chunks[1:]:

        previous_words = result[-1].split()

        overlap = previous_words[-CHUNK_OVERLAP_WORDS:]

        merged = " ".join(overlap + chunk.split())

        result.append(merged)

    return result


def create_chunks(page: Document) -> list[Document]:
    """
    Vytvorí chunky z jednej strany PDF.
    """

    if not page.text.strip():
        return []

    paragraphs = split_into_paragraphs(page.text)

    raw_chunks = []

    for paragraph in paragraphs:

        word_count = len(paragraph.split())

        if word_count <= CHUNK_SIZE_WORDS:

            raw_chunks.append(paragraph)

        else:

            raw_chunks.extend(
                split_large_paragraph(paragraph)
            )

    raw_chunks = apply_overlap(raw_chunks)

    documents = []

    for chunk in raw_chunks:

        documents.append(

            Document(

                author=page.author,

                book=page.book,

                page=page.page,

                text=chunk

            )

        )

    return documents