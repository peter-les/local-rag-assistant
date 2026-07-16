from models import SearchResult

from config import TOP_K

from embeddings import create_embedding

from vector_store import get_collection

from vector_store import search


def retrieve(

        question,

        search_filter=None

):

    collection = get_collection()

    embedding = create_embedding(question)

    top_k = TOP_K
	
    if (
        search_filter is not None and
        search_filter.top_k is not None
    ):
        top_k = search_filter.top_k

    raw = search(

        collection,

        embedding,

        top_k,

        search_filter

    )

    documents = raw["documents"][0]

    metadatas = raw["metadatas"][0]

    distances = raw["distances"][0]

    results = []

    for doc, meta, dist in zip(

            documents,

            metadatas,

            distances

    ):

        results.append(

            SearchResult(

                author=meta["author"],

                book=meta["book"],

                page=meta["page"],

                text=doc,

                distance=dist

            )

        )

    return results