from dataclasses import dataclass
from dataclasses import asdict
from dataclasses import field

from summarize_gutenberg.db import DB

@dataclass
class Book:
    id: int = field(default=None)
    title: str = None
    author: str = None
    url: str = None
    filename: str = None

    @classmethod
    def from_dict(cls, d):
        return Book(**d)
    def to_dict(self):
        return asdict(self)



class BooksDB:
    def __init__(self, db_path):
        self._db_path = db_path
        self._db = DB(db_path, ".books_db")

    def add_book(self, book: Book) -> int:
        """Add a book, return its id."""
        id = self._db.create(book.to_dict())
        self._db.update(id, {"id": id})
        return id

    def get_book(self, book_id: int) -> Book:
        """Return a book with a matching id."""
        db_item = self._db.read(book_id)
        if db_item is not None:
            return Book.from_dict(db_item)
        # else:
            # raise InvalidBookId(book_id)

    def list_books(self):
        """Return a list of books."""
        all = self._db.read_all()
        return [Book.from_dict(t) for t in all]

    def count(self) -> int:
        """Return the number of books in db."""
        return self._db.count()

    def update_book(self, book_id: int, book_mods: Book) -> None:
        """Update a book with modifications."""
        # try:
        self._db.update(book_id, book_mods.to_dict())
        # except KeyError as exc:
        #     raise InvalidBookId(book_id) from exc

    def delete_book(self, book_id: int) -> None:
        """Remove a book from db with given book_id."""
        self._db.delete(book_id)
        # except KeyError as exc:
            # raise InvalidBookId(book_id) from exc

    def delete_all(self) -> None:
        """Remove all books from db."""
        self._db.delete_all()

    def close(self):
        self._db.close()

    def path(self):
        return self._db_path