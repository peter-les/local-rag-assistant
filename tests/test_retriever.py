from retriever import retrieve


question = input("Question: ")

results = retrieve(question)

print()

for i, result in enumerate(results):

    print("=" * 80)

    print(f"Result {i+1}")

    print(f"Distance : {result.distance:.4f}")

    print(f"Author   : {result.author}")

    print(f"Book     : {result.book}")

    print(f"Page     : {result.page}")

    print()

    print(result.text[:500])

    print()