import typer
from rich import print, box
from rich.prompt import Prompt
from rich.table import Table
from pathlib import Path
import ast

from get_books import remove_parens, author_parse, author_check, url_check, fetch_default_books, process_books

app = typer.Typer()

def default_books():
    filepath = Path('./files/default_books.txt')
    if filepath.exists():
        with open(filepath, 'r') as books_txt:
            book_content = books_txt.read()
        books = ast.literal_eval(book_content)
    else:
        print("[italic yellow]Retrieving default book data...[/italic yellow]")

        books = process_books(fetch_default_books())
        with open(filepath,'w') as data:  
            data.write(str(books))
    book_nums = [book for book in books]
    return books, book_nums

@app.command()
def default():
    books, book_nums = default_books()
    table = Table(title="Default Books")
    table.add_column('No.')
    table.add_column('[bold cyan]Title', max_width=75, no_wrap=False)
    table.add_column('[bold magenta]Author')
    table.add_column('[bold yellow]Fulltext URL')

    for book_num in book_nums:
        table.add_row(str(book_num), books[book_num]['title'], books[book_num]['author'], f"[yellow]{books[book_num]['url']}")
    print('\n')
    print(table)
    print('\n')


    