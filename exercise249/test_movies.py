import os
import random
import string

import pytest

from pybites.exercise249.movies import MovieDb

salt = ''.join(
    random.choice(string.ascii_lowercase) for i in range(20)
)
DB = os.path.join(os.getenv("TMP", "/tmp"), f'movies_{salt}.db')
# https://www.imdb.com/list/ls055592025/
DATA = [
    ("The Godfather", 1972, 9.2),
    ("The Shawshank Redemption", 1994, 9.3),
    ("Schindler's List", 1993, 8.9),
    ("Raging Bull", 1980, 8.2),
    ("Casablanca", 1942, 8.5),
    ("Citizen Kane", 1941, 8.3),
    ("Gone with the Wind", 1939, 8.1),
    ("The Wizard of Oz", 1939, 8),
    ("One Flew Over the Cuckoo's Nest", 1975, 8.7),
    ("Lawrence of Arabia", 1962, 8.3),
]
TABLE = 'movies'


@pytest.fixture
def db():
    # instantiate MovieDb class using above constants
    # do proper setup / teardown using MovieDb methods
    # https://docs.pytest.org/en/latest/fixture.html (hint: yield)
    database = MovieDb(DB, DATA, TABLE)
    database.init()
    yield database
    database.drop_table()


@pytest.mark.parametrize("params,expected_rows", [
    ({"title": "the"}, 5),
    ({"title": "the"}, 5),
    ({"year": 1939}, 2),
    ({"score_gt": 9}, 2)
])
def test_query(db, params, expected_rows):
    results = db.query(**params)
    assert len(results) == expected_rows


def test_add(db):
    new_ids = []
    new_ids.append(db.add("Test 1", 2020, 10))
    new_ids.append(db.add("Test 2", 2020, 10))
    new_ids.append(db.add("Test 3", 2020, 10))

    results = db.query(title="Test%", year=2020)

    assert len(results) == 3
    assert new_ids == [
        len(DATA) + 1,
        len(DATA) + 2,
        len(DATA) + 3, 
    ]


def test_delete(db):
    new_ids = []
    new_ids.append(db.add("Test 1", 2020, 10))
    new_ids.append(db.add("Test 2", 2020, 10))
    for new_id in new_ids:
        db.delete(new_id)

    results = db.query(score_gt=9.9)

    assert len(results) == 0