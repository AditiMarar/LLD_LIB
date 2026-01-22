from enum import Enum
from datetime import date
class BookStatus(Enum):
    AVAILABLE = "AVAILABLE"
    ISSUED = "ISSUED"

class Genre(Enum):
    FICTION = "FICTION"
    SCIENCE = "SCIENCE"
    HISTORY = "HISTORY"
    TECHNOLOGY = "TECHNOLOGY"


class BookType(Enum):
    NOVEL = "NOVEL"
    COMIC = "COMIC"
    TEXTBOOK = "TEXTBOOK"
    REFERENCE = "REFERENCE"

class Author:
    def __init__(self, author_id, name):
        self.author_id = author_id
        self.name = name


class Book:
    def __init__(self, isbn, title, author, genre, book_type):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.genre = genre
        self.book_type = book_type


class BookItem:
    def __init__(self, copy_id, book):
        self.copy_id = copy_id
        self.book = book
        self.status = BookStatus.AVAILABLE


class LibraryCard:
    def __init__(self, card_number):
        self.card_number = card_number
        self.active = True


class Member:
    def __init__(self, member_id, name, library_card):
        self.member_id = member_id
        self.name = name
        self.library_card = library_card
        self.issued_books = []

    def issue_book(self, book_item):
        self.issued_books.append(book_item)

    def return_book(self, book_item):
        self.issued_books.remove(book_item)


class Transaction:
    def __init__(self, transaction_id, book_item, member):
        self.transaction_id = transaction_id
        self.book_item = book_item
        self.member = member
        self.issue_date = date.today()
        self.return_date = None

    def close_transaction(self):
        self.return_date = date.today()



class Catalog:
    def __init__(self):
        self.book_items = {}

    def add_book_item(self, book_item):
        self.book_items[book_item.copy_id] = book_item

    def get_book_item(self, copy_id):
        return self.book_items.get(copy_id)

    def search_by_genre(self, genre):
        return [
            item for item in self.book_items.values()
            if item.book.genre == genre
        ]

    def search_by_type(self, book_type):
        return [
            item for item in self.book_items.values()
            if item.book.book_type == book_type
        ]



class Library:
    def __init__(self):
        self.catalog = Catalog()
        self.members = {}
        self.transactions = []

    def add_member(self, member):
        self.members[member.member_id] = member

    def get_member(self, member_id):
        return self.members.get(member_id)

    def add_transaction(self, transaction):
        self.transactions.append(transaction)


class IssueReturnService:
    def __init__(self, library):
        self.library = library

    def issue_book(self, copy_id, member_id):
        book_item = self.library.catalog.get_book_item(copy_id)
        member = self.library.get_member(member_id)

        if not book_item:
            raise Exception("Book copy not found")

        if not member:
            raise Exception("Member not found")

        if not member.library_card.active:
            raise Exception("Library card inactive")

        if book_item.status == BookStatus.ISSUED:
            raise Exception("Book already issued")

        if book_item.book.book_type == BookType.REFERENCE:
            raise Exception("Reference books cannot be issued")

        book_item.status = BookStatus.ISSUED
        member.issue_book(book_item)

        transaction = Transaction(
            len(self.library.transactions) + 1,
            book_item,
            member
        )
        self.library.add_transaction(transaction)

        print(f"Book issued successfully to {member.name}")

    def return_book(self, copy_id, member_id):
        book_item = self.library.catalog.get_book_item(copy_id)
        member = self.library.get_member(member_id)

        if book_item not in member.issued_books:
            raise Exception("This book was not issued to the member")

        book_item.status = BookStatus.AVAILABLE
        member.return_book(book_item)

        for txn in self.library.transactions:
            if txn.book_item == book_item and txn.return_date is None:
                txn.close_transaction()
                break

        print(f"Book returned successfully by {member.name}")

if __name__ == "__main__":
    library = Library()

    author = Author("A1", "Holly Jackson")

    book = Book(
        isbn="ISBN1",
        title="Good girls guide to murder",#must read ;)
        author=author,
        genre=Genre.FICTION,
        book_type=BookType.NOVEL
    )

    book_item = BookItem("COPY1", book)
    library.catalog.add_book_item(book_item)

    card = LibraryCard("CARD3004")
    member = Member("M1", "Aditi Ajay Marar", card)
    library.add_member(member)

    service = IssueReturnService(library)
    service.issue_book("COPY1", "M1")
    service.return_book("COPY1", "M1")
