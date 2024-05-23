import pytest
import requests

from summarize_gutenberg.get_books import fetch_default_books, process_books, author_check, url_check

def test_gutendex_api():
    base_url = 'https://gutendex.com/books?languages=en'
    book_request = requests.get(base_url, params={'q': 'requests+lang:en'})
    assert book_request.status_code == 200
    assert 'results' in book_request.json()
    assert len(book_request.json()['results']) == 32

def test_fetch_default_books_success(mocker):
    mock_response = mocker.Mock()
    mock_response.json.return_value = {'results': ['book1', 'book2']}
    mock_response.raise_for_status.return_value = None
    mocker.patch('requests.get', return_value=mock_response)

    books = fetch_default_books()
    assert books == ['book1', 'book2']

def test_fetch_default_books_http_error(mocker):
    mocker.patch('requests.get', side_effect=requests.exceptions.HTTPError("Http Error"))

    with pytest.raises(requests.exceptions.HTTPError):
        fetch_default_books()

def test_fetch_default_books_connection_error(mocker):
    mocker.patch('requests.get', side_effect=requests.exceptions.ConnectionError("Connection Error"))

    with pytest.raises(requests.exceptions.ConnectionError):
        fetch_default_books()

def test_fetch_default_books_timeout(mocker):
    mocker.patch('requests.get', side_effect=requests.exceptions.Timeout("Timeout Error"))

    with pytest.raises(requests.exceptions.Timeout):
        fetch_default_books()

def test_fetch_default_books_request_exception(mocker):
    mocker.patch('requests.get', side_effect=requests.exceptions.RequestException("Exotic Error"))

    with pytest.raises(requests.exceptions.RequestException):
        fetch_default_books()

test_authors_no_list = {
    'name': 'Doe, John'
}

test_authors_no_name = [
    {
    'mame': 'Doe, John'
    }
    ]

def test_author_check_no_list():
    with pytest.raises(KeyError) as excinfo:
        author_check(test_authors_no_list)
    assert "'authors' in unexpected format (should be list)" in str(excinfo.value)

def test_author_check_no_name():
    with pytest.raises(KeyError) as excinfo:
        author_check(test_authors_no_name)
    assert "No field named 'name' in authors" in str(excinfo.value)

test_formats_no_plaintext = {
    'wrong_format': 'book_url',
    }

def test_url_check_no_plaintext():
    with pytest.raises(KeyError) as excinfo:
        url_check(test_formats_no_plaintext)
    assert "No plaintext URL or plaintext key format has changed" in str(excinfo.value)

book_data = [
    # Normal data
    (
        {
            'id': 1,
            'title': 'Sample Book',
            'authors': [{'name': 'Doe, John'}],
            'formats': {'text/plain; charset=us-ascii': 'http://example.com'}
        },
        {
            1: {
                'title': 'Sample Book',
                'author': 'John Doe',
                'url': 'http://example.com',
                'filename': 'samplebook.txt',
            }
        }
    ),
    # No title
    (
        {
            'id': 1,
            'authors': [{'name': 'Doe, John'}],
            'formats': {'text/plain; charset=us-ascii': 'http://example.com'}
        },
        {
            1: {
                'title': None,
                'author': 'John Doe',
                'url': 'http://example.com',
                'filename': None,
            }
        }
    ),
    # No author
    (
        {
            'id': 1,
            'title': 'Sample Book',
            'formats': {'text/plain; charset=us-ascii': 'http://example.com'}
        },
        {
            1: {
                'title': 'Sample Book',
                'author': 'No author found.',
                'url': 'http://example.com',
                'filename': 'samplebook.txt',
            }
        }
    ),
    # No formats
    (
        {
            'id': 1,
            'title': 'Sample Book',
            'authors': [{'name': 'Doe, John'}]
        },
        {
            1: {
                'title': 'Sample Book',
                'author': 'John Doe',
                'url': 'No URLs found.',
                'filename': 'samplebook.txt',
            }
        }
    ),
    # No title or author
    (
        {
            'id': 1,
            'formats': {'text/plain; charset=us-ascii': 'http://example.com'}
        },
        {
            1: {
                'title': None,
                'author': 'No author found.',
                'url': 'http://example.com',
                'filename': None,
            }
        }
    ),
    # no title or formats
    (
        {
            'id': 1,
            'authors': [{'name': 'Doe, John'}],
        },
        {
            1: {
                'title': None,
                'author': 'John Doe',
                'url': 'No URLs found.',
                'filename': None,
            }
        }
    ),
    # no author or formats
    (
        {
            'id': 1,
            'title': 'Sample Book',
        },
        {
            1: {
                'title': 'Sample Book',
                'author': 'No author found.',
                'url': 'No URLs found.',
                'filename': 'samplebook.txt',
            }
        }
    ),
    # no title author or formats
    (
        {
            'id': 1,
        },
        {
            1: {
                'title': None,
                'author': 'No author found.',
                'url': 'No URLs found.',
                'filename': None,
            }
        }
    ),
]


@pytest.mark.parametrize('input, expected', book_data)
def test_process_books(input, expected):
    result = process_books([input])
    assert result == expected, f'Expected {expected}, but got {result}'