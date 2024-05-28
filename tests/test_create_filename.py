import pytest
from summarize_gutenberg.get_books import create_filename

titles = [
    ('Dracula', 'dracula.txt'), # one word
    ('Franny and Zooey', 'frannyandzooey.txt'), # spaces
    ('Frankenstein; Or, The Modern Prometheus', 'frankenstein.txt'), # semicolon
    ('"Left-Wing" Communism: an Infantile Disorder', 'leftwingcommunism.txt'), # colon, quoation marks, hyphen
    ('We Who Are About To...', 'wewhoareaboutto.txt'), # periods
    ("Swann's Way", 'swannsway.txt'), # apostrophe/single quote
    ("My Life — Volume 1", 'mylifevolume1.txt') # em dash which is weird but one of the top gutenberg books has one
]

@pytest.mark.parametrize('input, expected', titles)
def test_create_filename(input, expected):
    assert create_filename(input) == expected, f'Expected {expected}, but got {create_filename(input)}'