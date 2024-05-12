import pytest
from pathlib import Path
from tempfile import TemporaryDirectory
import ipdb

from ..api import Book, BooksDB

@pytest.fixture()
def books_db():
    with TemporaryDirectory() as db_dir:
        db_path = Path(db_dir)
        db = BooksDB(db_path)
        yield db
        db.close()

def test_empty_db(books_db):
    assert books_db.count() == 0

def test_add_one_book(books_db):
    books_db.add_book(Book())

    assert books_db.count() == 1

def test_add_two_books(books_db):
    books_db.add_book(Book())
    books_db.add_book(Book())

    assert books_db.count() == 2

def test_delete_book(books_db):
    books_db.add_book(Book(id=1))
    books_db.add_book(Book(id=2))
    books_db.delete_book(2)

    assert books_db.count() == 1

def test_delete_all(books_db):
    books_db.add_book(Book(id=1))
    books_db.add_book(Book(id=2))
    books_db.delete_all()

    assert books_db.count() == 0

def test_get_book(books_db, book_fixture):
    book = book_fixture
    books_db.add_book(book)
    gotten_book = books_db.get_book(1)
    
    assert book == gotten_book