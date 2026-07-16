# test_chunker.py
from pdf_loader import load_all_books
from chunker import create_chunks

pages = load_all_books("../corpora/spiritual")

chunks = create_chunks(pages[0])

print(f"Počet chunkov: {len(chunks)}")
print()

for chunk in chunks:

    print("=" * 80)

    print("Author :", chunk.author)

    print("Book   :", chunk.book)

    print("Page   :", chunk.page)

    print()

    print(chunk.text[:300])

    print()