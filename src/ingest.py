#ingest.py
from pdf_loader import load_all_books
from chunker import create_chunks
from embeddings import create_embedding

from vector_store import (
    reset_database,
    add_document
)

from config import BOOKS_PATH


print()

print("Loading books...")

pages = load_all_books(
    BOOKS_PATH + "/spiritual"
)

print(f"Pages loaded: {len(pages)}")

collection = reset_database()

counter = 0

for page in pages:

    chunks = create_chunks(page)

    for chunk in chunks:

        if not chunk.text.strip():
            continue

        embedding = create_embedding(
            chunk.text
        )

        add_document(
            collection,
            chunk,
            embedding,
            counter
        )

        counter += 1

print()

print("Embedding finished.")

print(f"Indexed chunks: {counter}")