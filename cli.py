import typer
from rich import print, box
from rich.prompt import Prompt
from rich.table import Table
from pathlib import Path
import ast

from get_books import remove_parens, author_parse, author_check, url_check, fetch_default_books, process_books

app = typer.Typer()

def default_books():
    books = process_books(fetch_default_books())
    ids = {book for book in books}
    return books, ids

@app.command()
def default():
    filepath = Path('./files/default_books.txt')
    if filepath.exists():
        with open(filepath, 'r') as books_txt:
            book_content = books_txt.read()
        books = ast.literal_eval(book_content)
        ids = {book for book in books}
    else:
        books, ids = default_books()
        with open(filepath,'w') as data:  
            data.write(str(books))

    table = Table(title="Default Books")
    table.add_column('[bold cyan]Title', max_width=75, no_wrap=False)
    table.add_column('[bold magenta]Author')

    for book_id in ids:
        table.add_row(books[book_id]['title'], books[book_id]['author'])
    print('\n')
    print(table)
    print('\n')


    