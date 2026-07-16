#test_rag.py
from rag import retrieve

while True:

    q = input("> ")

    doc = retrieve(q)

    if doc is None:
        print("I don't know answer this question.")
    else:
        print(doc)