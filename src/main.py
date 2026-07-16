#main.py
from conversation import Conversation
from commands import (
    print_authors,
    print_books,
    print_status
)
from search_filter import SearchFilter
from rag import ask

conversation = Conversation()
print()
print("WisdomRAG")
print("Type 'exit' to quit.")
print()

current_filter = SearchFilter()

while True:
    question = input("> ")
    if question.lower() == "exit":
        break

    if question == "/authors":
        print_authors()
        continue

    if question == "/books":
        print_books()
        continue

    if question == "/status":
        print_status(current_filter)
        continue

    if question.startswith("/author "):
        author = question[8:].strip()
        if author.lower() == "all":
            current_filter.authors = None
            print("Using all authors.\n")
        else:
            authors = [
                a.strip()
                for a in author.split(",")
            ]
            current_filter.authors = authors
            print()
            print("Selected authors:")
            for a in authors:
                print("-", a)
            print()
        continue

    if question.startswith("/book "):
        book = question[6:].strip()
        if book.lower() == "all":
            current_filter.books = None
            print("Using all books.\n")
        else:
            books = [
                b.strip()
                for b in book.split(",")
            ]
            current_filter.books = books
            print()
            print("Selected books:")
            for b in books:
                print("-", b)
            print()
        continue

    #print() # Prázdny riadok pred odpoveďou, aby to pekne vyzeralo
    conversation.add_user(question)
    # Spustíme generátor a okamžite vypisujeme kúsky odpovede, ako prichádzajú
    answer = ""

    for chunk in ask(question, current_filter, conversation, debug=True):

        answer += chunk

        print(chunk, end="", flush=True)

    # Pred uložením do histórie odstránime automatické citácie, ktoré pridal rag.py na koniec streamu
    if "\n\nSources" in answer:
        answer = answer.split("\n\nSources")[0]
	
    conversation.add_assistant(answer)

    print("\n") # Na konci odpovede skočíme na nový riadok a urobíme miesto pre ďalšiu otázku