import pytest
from ..api import Book

@pytest.fixture()
def book_fixture():
    """
    Create a Book.
    """
    book = Book(
        id=1,
        title="yesterday's tomorrow",
        short_title="yesterdaystomorrow",
        author="Wilfred Sinecure",
        url="https://www.gutenberg.org/",
        filepath=None
    )

    return book

def test_book_field_access(book_fixture):
    book = book_fixture

    assert book.title == "yesterday's tomorrow"
    assert book.short_title == "yesterdaystomorrow"
    assert book.title == "yesterday's tomorrow"
    assert book.url == "https://www.gutenberg.org/"
    assert book.filepath is None

def test_book_defaults():
    book = Book()

    assert book.title is None
    assert book.short_title is None
    assert book.title is None
    assert book.url is None
    assert book.filepath is None