from summarize_gutenberg.api import Book

def test_book_field_access(book_fixture):
    book = book_fixture

    assert book.id == 1
    assert book.title == "Yesterday's Tomorrows"
    assert book.author == "Wilfred Sinecure"
    assert book.url == "https://www.gutenberg.org/"
    assert book.filename == "yesterdaystomorrows.txt"

def test_book_defaults():
    book = Book()

    assert book.title is None
    assert book.author is None
    assert book.url is None
    assert book.filename is None

def test_from_dict(book_fixture):
    book1 = book_fixture
    book2_dict = {
        "id": 1,
        "title": "Yesterday's Tomorrows",
        "author": "Wilfred Sinecure",
        "url": "https://www.gutenberg.org/",
        "filename": "yesterdaystomorrows.txt",
    }
    book2 = Book.from_dict(book2_dict)

    assert book1 == book2

def test_to_dict(book_fixture):
    book1 = book_fixture
    book_dict = book1.to_dict()
    expected =  {
        "id": 1,
        "title": "Yesterday's Tomorrows",
        "author": "Wilfred Sinecure",
        "url": "https://www.gutenberg.org/",
        "filename": "yesterdaystomorrows.txt",
    }

    assert book_dict == expected