from pprint import pprint  # 1. Týmto importujeme "pekné tlačenie"
from pdf_loader import load_all_books


docs = load_all_books("../corpora/spiritual")

print("Počet strán:", len(docs))

print()

#print(docs[100])
# 2. Tu sme zmenili print na pprint a pridali formátovanie
pprint(docs[100], width=80, sort_dicts=False) #