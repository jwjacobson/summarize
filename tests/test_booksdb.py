import pytest
from pathlib import Path
from tempfile import TemporaryDirectory

from ..api import BooksDB

@pytest.fixture()
def books_db():
    with TemporaryDirectory() as db_dir:
        db_path = Path(db_dir)
        db = BooksDB(db_path)
        yield db
        db.close()

def test_empty_db(books_db):
    assert books_db.count() == 0
