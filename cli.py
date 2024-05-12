import typer
from rich import print, box
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.table import Table
from pathlib import Path
import ast
from contextlib import contextmanager
from dataclasses import dataclass

from get_books import fetch_default_books, process_books
from get_text import write_text_to_file
from make_summary import save_summary, print_summary

FILE_DIR = "./files/"
SUMMARY_DIR = "./files/summaries/"



app = typer.Typer()

def default_books():
    default_books_filepath = Path(FILE_DIR+'default_books.txt')
    if default_books_filepath.exists():
        with open(default_books_filepath, 'r') as books_txt:
            book_content = books_txt.read()
        books = ast.literal_eval(book_content)
    else:
        print("[italic yellow]Retrieving default book data...[/italic yellow]")

        books = process_books(fetch_default_books())
        with open(default_books_filepath,'w') as data:  
            data.write(str(books))
    book_nums = [book for book in books]
    return books, book_nums

@app.command()
def default():
    books, book_nums = default_books()
    table = Table(box=box.SQUARE_DOUBLE_HEAD, border_style="magenta")
    table.add_column('No.')
    table.add_column('[bold cyan]Title', max_width=75, no_wrap=False)
    table.add_column('[bold magenta]Author')
    table.add_column('[bold yellow]Fulltext URL')

    for book_num in book_nums:
        table.add_row(str(book_num), books[book_num]['title'], books[book_num]['author'], f"[yellow]{books[book_num]['url']}")
    print('\n')
    print(table)
    print('\n')

    choice = Prompt.ask("Select a book by number")
    while int(choice) < 1 or int(choice) > 32:
        choice = Prompt.ask("[red]Please choose a number between 1 and 32")
    chosen_book = books[int(choice)]
    
    print(f"You have chosen [bold cyan]{chosen_book['title']}[/bold cyan] by [bold magenta]{chosen_book['author']}[/bold magenta].")
    filepath = Path(FILE_DIR+choice+chosen_book['short_title']+'.txt')

    if filepath.exists():
        print(f"The book has previously been saved to {filepath}.")
    else:
        print("[italic yellow]\nRetrieving book text...[/italic yellow]")
        chosen_book['filepath'] = write_text_to_file(chosen_book['url'], filepath)
        print(f"\nText of {chosen_book['title']} saved to {chosen_book['filepath']}.")

    choice = Prompt.ask("\nDo you want to print or save your summary?", choices=['print', 'save'], default='save')
    chunks = IntPrompt.ask("How many lines per chunk?", default=400)

    if chunks < 50:
        print("[red bold]Warning[/red bold]: choosing a low value could take a lot of time and resources.")
        confirmation = Confirm.ask("Are you sure?")
        
    if choice == 'print':
        print_summary(filepath, chunks)
    else:
        target_filepath = Path(SUMMARY_DIR+chosen_book['short_title']+f'_{chunks}_sum.txt')
        save_summary(filepath, target_filepath, chunks)
        print(f'\nSummary saved to {target_filepath}.')

@contextmanager
def books_db():
    db_path = get_path()
    db = books.BooksDB(db_path)
    yield db
    db.close()


