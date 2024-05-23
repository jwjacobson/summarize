import pytest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / "src"))

from summarize_gutenberg.api import Book

@pytest.fixture()
def book_fixture():
    """
    Create a Book.
    """
    book = Book(
        id=1,
        title="Yesterday's Tomorrows",
        author="Wilfred Sinecure",
        url="https://www.gutenberg.org/",
        filename="yesterdaystomorrows.txt",
    )

    return book