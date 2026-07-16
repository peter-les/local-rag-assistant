from vector_store import get_all_authors
from vector_store import get_all_books


def print_authors():

    print()

    print("Available authors")

    print("-----------------")

    for author in get_all_authors():

        print(author)

    print()


def print_books():

    print()

    print("Available books")

    print("---------------")

    for book in get_all_books():

        print(book)

    print()


def print_status(search_filter):

    print()

    print("Current settings")

    print("----------------")

    if search_filter.authors is None:

        print("Authors : ALL")

    else:

        print("Authors :", ", ".join(search_filter.authors))

    if search_filter.books is None:

        print("Books   : ALL")

    else:

        print("Books   :", ", ".join(search_filter.books))

    print()