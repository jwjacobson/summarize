import os
import typer
from rich import print, box
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.table import Table
from pathlib import Path
from contextlib import contextmanager

from summarize.get_books import fetch_default_books, process_books
from summarize.get_text import write_text_to_file
from summarize.make_summary import save_summary, print_summary
from summarize.api import Book, BooksDB

import ipdb

FILE_DIR = Path("./files/")
SUMMARY_DIR = FILE_DIR / "summaries"

app = typer.Typer()

def create_filepath(book_dict):
    return f'{book_dict['short_title']}.txt'

def get_default_books():
    print("\n[italic yellow]Retrieving default book data...")
    books = process_books(fetch_default_books())
    for book in books:
        book_dict = books[book]
        book_dict['filepath'] = str(create_filepath(book_dict))
        with books_db() as db:
            db.add_book(Book.from_dict(books[book]))
    
@app.command()
def default():
    get_default_books()

    table = Table(box=box.SQUARE_DOUBLE_HEAD, border_style="magenta")
    table.add_column('No.')
    table.add_column('[bold cyan]Title', max_width=75, no_wrap=False)
    table.add_column('[bold magenta]Author')
    table.add_column('[bold yellow]Fulltext URL')

    with books_db() as db:
        books = db.list_books()
        for order_num, book in enumerate(books, start=1):
            table.add_row(f'{str(order_num)}.', book.title, book.author, f"[yellow]{book.url}")
            order_num += 1
    print('\n')
    print(table)
    print('\n')

    max_choice = len(books)
    choice = Prompt.ask("Select a book by number")
    while not choice.isdigit() or int(choice) < 1 or int(choice) > max_choice:
        choice = Prompt.ask("[red]Please choose a number between 1 and 32")

    selected_book = books[int(choice) - 1]
    
    print(f"\nYou have chosen [bold cyan]{selected_book.title}[/bold cyan] by [bold magenta]{selected_book.author}[/bold magenta].")
    filepath = FILE_DIR / Path(selected_book.filepath)

    if filepath.exists():
        print(f"The book has previously been saved to {filepath}.")
    else:
        print("[italic yellow]\nRetrieving book text...[/italic yellow]")
        write_text_to_file(selected_book.url, filepath)
        print(f"\nText of {selected_book.title} saved to {filepath}.")

    choice = Prompt.ask("\nDo you want to print or save your summary?", choices=['print', 'save'], default='save')
    chunks = IntPrompt.ask("How many lines per chunk?", default=400)

    if chunks < 50:
        print("[red bold]Warning[/red bold]: choosing a low value could take a lot of time and resources.")
        confirmation = Confirm.ask("Are you sure?")
        
    if choice == 'print':
        print_summary(filepath, chunks)
    else:
        target_filepath = SUMMARY_DIR / Path(selected_book.filepath)

        save_summary(filepath, target_filepath, chunks)
        print(f'\nSummary saved to {target_filepath}.')

    with books_db() as db:
        db.delete_all()

def get_path():
    db_path_env = os.getenv("BOOKS_DB_DIR", "")
    if db_path_env:
        db_path = Path(db_path_env)
    else:
        db_path = Path(__file__).parent / "books_db"
    return db_path

@contextmanager
def books_db():
    db_path = get_path()
    db = BooksDB(db_path)
    try:
        yield db
    finally:
        db.close()


