from vector_store import get_collection

collection = get_collection()

# Vyžiadame si z databázy konkrétne strany 86, 98 a pre porovnanie aj 99
response = collection.get(
    where={
        "$and": [
            {"author": "Eckhart Tolle"},
            {"page": {"$in": [24, 86, 98, 99]}}
        ]
    },
    include=["documents", "metadatas"]
)

documents = response["documents"]
metadatas = response["metadatas"]

print(f"Nájdených záznamov v DB pre tieto strany: {len(documents)}\n")

for doc, meta in zip(documents, metadatas):
    print("=" * 60)
    print(f"Kniha: {meta['book']} | Strana: {meta['page']}")
    print("-" * 60)
    # Vypíšeme prvých 300 znakov, aby sme videli, či tam ten text naozaj je
    print(doc[:300] + "...")
    print()