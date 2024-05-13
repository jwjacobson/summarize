import pytest
from summarize.get_books import abbreviate_title

titles = [
    ('Dracula', 'dracula'), # one word
    ('Franny and Zooey', 'frannyandzooey'), # spaces
    ('Frankenstein; Or, The Modern Prometheus', 'frankenstein'), # semicolon
    ('"Left-Wing" Communism: an Infantile Disorder', 'leftwingcommunism'), # colon, quoation marks, hyphen
    ('We Who Are About To...', 'wewhoareaboutto'), # periods
    ("Swann's Way", 'swannsway'), # apostrophe/single quote
    ("My Life — Volume 1", 'mylifevolume1') # em dash which is weird but one of the top gutenberg books has one
]

@pytest.mark.parametrize('input, expected', titles)
def test_abbreviate_title(input, expected):
    assert abbreviate_title(input) == expected, f'Expected {expected}, but got {abbreviate_title(input)}'