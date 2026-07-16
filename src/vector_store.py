#vector_store.py
import chromadb

from config import CHROMA_PATH


COLLECTION_NAME = "wisdomrag"


client = chromadb.PersistentClient(path=CHROMA_PATH)


def get_collection():

    return client.get_or_create_collection(
        name=COLLECTION_NAME
    )


def reset_database():

    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    return get_collection()


def add_document(collection, document, embedding, doc_id):

    collection.add(

        ids=[str(doc_id)],

        embeddings=[embedding],

        documents=[document.text],

        metadatas=[

            {
                "author": document.author,
                "book": document.book,
                "page": document.page
            }

        ]

    )


def search(

        collection,

        embedding,

        top_k,

        search_filter=None

):

    where = None

    if search_filter is not None:

        conditions = []

        if search_filter.authors:

            if len(search_filter.authors) == 1:

                conditions.append({
                    "author": search_filter.authors[0]
                })

            else:

                conditions.append({
                    "author": {
                        "$in": search_filter.authors
                    }
                })

        if search_filter.books:

            if len(search_filter.books) == 1:

                conditions.append({
                    "book": search_filter.books[0]
                })

            else:

                conditions.append({
                    "book": {
                        "$in": search_filter.books
                    }
                })

        if len(conditions) == 1:

            where = conditions[0]

        elif len(conditions) > 1:

            where = {
                "$and": conditions
            }

    return collection.query(

        query_embeddings=[embedding],

        n_results=top_k,

        where=where,

        include=[

            "documents",

            "metadatas",

            "distances"

        ]

    )
	
def get_all_metadata():
	
	# Oprava: Získame kolekciu pred jej použitím
    collection = get_collection()

    data = collection.get(
        include=["metadatas"]
    )

    return data["metadatas"]


def get_all_authors():

    authors = set()

    for metadata in get_all_metadata():

        authors.add(metadata["author"])

    return sorted(authors)


def get_all_books():

    books = set()

    for metadata in get_all_metadata():

        books.add(metadata["book"])

    return sorted(books)