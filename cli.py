import typer
from rich import print, box
from rich.prompt import Prompt, IntPrompt
from rich.table import Table
from pathlib import Path
import ast

from get_books import fetch_default_books, process_books
from get_text import write_text_to_file

FILE_DIR = "./files/"

app = typer.Typer()

def default_books():
    filepath = Path(FILE_DIR+'default_books.txt')
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
    filepath = FILE_DIR+choice+chosen_book['short_title']+'.txt'
    print("[italic yellow]\nRetrieving book text...[/italic yellow]")
    write_text_to_file(chosen_book['url'], filepath)


    