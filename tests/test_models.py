from ..api import Book

def test_book_field_access(book_fixture):
    book = book_fixture

    assert book.id == 1
    assert book.title == "Yesterday's Tomorrows"
    assert book.short_title == "yesterdaystomorrows"
    assert book.author == "Wilfred Sinecure"
    assert book.url == "https://www.gutenberg.org/"
    assert book.filepath is None

def test_book_defaults():
    book = Book()

    assert book.title is None
    assert book.short_title is None
    assert book.title is None
    assert book.url is None
    assert book.filepath is None

def test_from_dict(book_fixture):
    book1 = book_fixture
    book2_dict = {
        "id": 1,
        "title": "Yesterday's Tomorrows",
        "short_title": "yesterdaystomorrows",
        "author": "Wilfred Sinecure",
        "url": "https://www.gutenberg.org/",
        "filepath": None
    }
    book2 = Book.from_dict(book2_dict)

    assert book1 == book2

def test_to_dict(book_fixture):
    book1 = book_fixture
    book_dict = book1.to_dict()
    expected =  {
        "id": 1,
        "title": "Yesterday's Tomorrows",
        "short_title": "yesterdaystomorrows",
        "author": "Wilfred Sinecure",
        "url": "https://www.gutenberg.org/",
        "filepath": None
    }

    assert book_dict == expected