import pytest
from data_processing.get_books import author_parse

authors = [
('Anonymous', 'Anonymous'), # single name
('Austen, Jane', 'Jane Austen'), # first & last
('Stevenson, Robert Louis', 'Robert Louis Stevenson'), # first last middle
('Chesterton, G. K. (Gilbert Keith)', 'G. K. Chesterton'), # parenthetical
('H. D. (Hilda Doolittle)', 'H. D.'), # irregular parenthetical
('Tolkien, J. R. R. (John Ronald Reuel)', 'J. R. R. Tolkien'), # parenthetical with three initials
('Von Arnim, Elizabeth', 'Elizabeth Von Arnim'), # von
('Sanchez, Nellie Van de Grift', 'Nellie Van de Grift Sanchez'), # van
('Martinez de la Torre, Rafael', 'Rafael Martinez de la Torre'), # de la 1
('Cervantes Saavedra, Miguel de', 'Miguel de Cervantes Saavedra'), # de
('Alger, Horatio, Jr.', 'Horatio Alger Jr.'), # jr
(None, '') # none
]

@pytest.mark.parametrize('input, expected', authors)
def test_author_parse(input, expected):
    assert author_parse(input) == expected, f'Expected {expected}, but got {author_parse(input)}'