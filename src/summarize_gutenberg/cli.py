import os
import typer
from rich import print, box
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.table import Table
from pathlib import Path
from contextlib import contextmanager

from summarize_gutenberg.get_books import fetch_default_books, process_books
from summarize_gutenberg.get_text import write_text_to_file
from summarize_gutenberg.make_summary import save_summary, print_summary
from summarize_gutenberg.api import Book, BooksDB

FILE_DIR = Path("./files/")
SUMMARY_DIR = FILE_DIR / "summaries"

def dir_check():
    """Make sure the directories for saving files exist"""
    FILE_DIR.mkdir(parents=True, exist_ok=True)
    SUMMARY_DIR.mkdir(parents=True, exist_ok=True)

dir_check()

app = typer.Typer()


def get_default_books():
    """
    Get the default book info then populate the database with corresponding Book objects
    """
    print("\n[italic yellow]Retrieving default book data...")
    books = process_books(fetch_default_books())
    for book in books:
        with books_db() as db:
            db.add_book(Book.from_dict(books[book]))
    
@app.command()
def default():
    """
    Default behavior when given no CLI options: get the 32 most popular books and guide the user interactively through the summarization process.
    """
    with books_db() as db:
        book_count = db.count()
        if book_count:  # If there are any books in the db at this point they are leftover from previous incomplete executions
            db.delete_all()

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
    filepath = FILE_DIR / Path(selected_book.filename)

    if filepath.exists():
        print(f"The book has previously been saved to {filepath}.")
    else:
        print("[italic yellow]\nRetrieving book text...[/italic yellow]")
        write_text_to_file(selected_book.url, filepath)
        print(f"\nText of {selected_book.title} saved to {filepath}.")

    choice = Prompt.ask("\nDo you want to [P]rint or [S]ave your summary?", choices=['p', 's'])
    chunks = IntPrompt.ask("How many lines per chunk?", default=400)

    # if chunks < 50:
    #     print("[red bold]Warning[/red bold]: choosing a low value could take a lot of time and resources.")
    #     confirmation = Confirm.ask("Are you sure?")
        
    if choice == 'p':
        print_summary(filepath, chunks)
    else:
        target_filepath = SUMMARY_DIR / Path(selected_book.filename)
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


