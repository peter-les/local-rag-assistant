import ollama

from config import EMBEDDING_MODEL


def create_embedding(text):

    response = ollama.embed(

        model=EMBEDDING_MODEL,

        input=text

    )

    return response["embeddings"][0]