from models import Document
from text_cleaner import clean_text
from pathlib import Path
import fitz


def load_all_books(corpus_path):
    """
    Načíta všetky PDF v korpuse.

    Returns:
        list dokumentov
    """

    documents = []

    corpus = Path(corpus_path)

    for author_dir in corpus.iterdir():

        if not author_dir.is_dir():
            continue

        author = author_dir.name

        for pdf in author_dir.glob("*.pdf"):

            documents.extend(
                load_single_pdf(pdf, author)
            )

    return documents


def load_single_pdf(pdf_path, author):

    pdf = fitz.open(pdf_path)

    pages = []

    for page_number in range(len(pdf)):

        page = pdf.load_page(page_number)

        text = clean_text(
            page.get_text("text")
        )

        pages.append(

            Document(

                author=author,

                book=pdf_path.stem,

                page=page_number + 1,

                text=text

            )

        )

    pdf.close()

    return pages