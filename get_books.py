"""
This module contains functions for fetching the first page of English-language results from the Gutendex API and creating a dictionary for each book,
in which the key is the book's ID and the value is a dictionary containing title, author, and a download link.
Author names are converted to First Middle Last format.
"""

import requests


def remove_parens(author):
    """
    Remove parentheticals from an author's name, for passing back to author_parse function
    """
    author = author.split()
    for name in author:
        if name[0] == "(":
            total_parens = len(author) - author.index(name)
    return " ".join(author[:-total_parens])


def author_parse(author):
    """
    Take the author information which is stored in Last, First Middle format and convert it to First Middle Last.
    For now it only handles the first author, so second authors of multiauthor books are out of luck.
    Examples:
    'Shelley, Mary Wollstonecraft' -> 'Mary Wollstonecraft Shelley'
    'Von Arnim, Elizbeth' -> 'Elizbeth Von Arnim'
    """
    if not author:
        return ""

    if author[-1] == ")":
        author = remove_parens(author)

    split_author = author.split(",")

    if len(split_author) == 1:  # One-name authors require no processing
        return author
    elif (
        len(split_author) == 2
    ):  # Presence of only one comma implies 'conventional' name structure (last + first [+ middle])
        return split_author[1].lstrip() + " " + split_author[0]
    else:  # Presence of more than one comma implies a suffix like "Jr."
        return split_author[1].lstrip() + " " + split_author[0] + " " + split_author[2].lstrip()


def author_check(authors):
    """
    Find and return a book's (first) author.
    """
    if not authors:
        return "No author found."

    try:
        name_dict = authors[0]
    except KeyError as e:
        raise KeyError(f"'authors' in unexpected format (should be list)\nOriginal error: {e}")

    try:
        author = name_dict["name"]
    except KeyError as e:
        raise KeyError(f"No field named 'name' in authors\nOriginal error: {e}")

    return author


def url_check(formats):
    """
    Find and return a book's full-text url.
    """
    if not formats:
        return "No URLs found."

    try:
        url = formats["text/plain; charset=us-ascii"]
    except KeyError as e:
        raise KeyError(f"No plaintext URL or plaintext key format has changed\nOriginal error: {e}")

    return url

def abbreviate_title(title):
    """
    Produces a shortened lowercase title with no spaces or punctuation, for use in filenames.
    """
    res_list = []
    colons = {':', ';'}
    puncts = {',', ' ', '.', '—', "'"}

    for char in title:
        if char in colons:
            break
        elif char in puncts:
            continue
        else:
            res_list.append(char.lower())

    return ''.join(res_list)    

def fetch_default_books():
    """
    Download info of the 32 most popular books on Project Gutenberg and return a json of them.
    """
    base_url = "https://gutendex.com/books?languages=en"

    try:
        book_request = requests.get(base_url, params={"q": "requests+lang:en"})
        book_request.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
        raise
    except requests.exceptions.ConnectionError as errc:
        print("Connection error:", errc)
        raise
    except requests.exceptions.Timeout as errt:
        print("Timeout error:", errt)
        raise
    except requests.exceptions.RequestException as err:
        print("Exotic error:", err)
        raise

    books = book_request.json()["results"]

    return books


def process_books(books):
    """
    Create a dictionary of fetched books where the key is an id number and the value contains title, abbreviated title, author, and full-text url.
    """
    book_data = {}
    book_num = 1
    for book in books:
        title = book.get("title", None)

        if title:
            short_title = abbreviate_title(title)
        else:
            short_title = None

        authors = book.get("authors")
        author = author_parse(author_check(authors))

        formats = book.get("formats")
        url = url_check(formats)

        book_data[book_num] = {"title": title, "short_title": short_title, "author": author, "url": url}
        book_num += 1

    return book_data

if __name__ == "__main__":
    books = process_books(fetch_default_books())
    book_list = [book for book in books]
    for book in book_list:
        print(books[book]['short_title'])
