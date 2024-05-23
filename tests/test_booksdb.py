import pytest
from pathlib import Path
from tempfile import TemporaryDirectory

from summarize_gutenberg.api import Book, BooksDB

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

def test_list_books(books_db):
    books_db.add_book(Book(id=1))
    books_db.add_book(Book(id=2))
    books_db.add_book(Book(id=3))
    listed_books = books_db.list_books()
    expected_ids = {1, 2, 3}

    assert len(listed_books) == 3
    for book in listed_books:
        assert book.id in expected_ids

def test_update_book(books_db, book_fixture):
    book = book_fixture
    books_db.add_book(book)
    new_data = {
        "title": "Tomorrow's Yesterdays",
        "author": "Clifton Semaphore",
        "url": "https://www.csemaphore.com/2",
        "filename": "tomorrowsyesterdays.txt",
    }

    new_book = Book.from_dict(new_data)
    books_db.update_book(book.id, new_book)
    updated_book_data = books_db.get_book(book.id).to_dict()

    assert updated_book_data['id'] == book.id
    assert updated_book_data['title'] == new_data['title']
    assert updated_book_data['author'] == new_data['author']
    assert updated_book_data['url'] == new_data['url']
    assert updated_book_data['filename'] == new_data['filename']




