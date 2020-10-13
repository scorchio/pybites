from dataclasses import dataclass
from operator import attrgetter
from pathlib import Path
from urllib.request import urlretrieve

from bs4 import BeautifulSoup

url = ("https://bites-data.s3.us-east-2.amazonaws.com/"
       "best-programming-books.html")
tmp = Path("/tmp")
html_file = tmp / "books.html"

if not html_file.exists():
    urlretrieve(url, html_file)


@dataclass
class Book:
    """Book class should instatiate the following variables:

    title - as it appears on the page
    author - should be entered as lastname, firstname
    year - four digit integer year that the book was published
    rank - integer rank to be updated once the books have been sorted
    rating - float as indicated on the page
    """
    title: str
    author: str
    year: int
    rank: int
    rating: float

    def __str__(self):
        return f'[{self.rank:0>3}] {self.title} ({self.year})\n      {self.author} {self.rating}'

def _get_soup(file):
    return BeautifulSoup(file.read_text(), "html.parser")


def display_books(books, limit=10, year=None):
    """Prints the specified books to the console

    :param books: list of all the books
    :param limit: integer that indicates how many books to return
    :param year: integer indicating the oldest year to include
    :return: None
    """
    books_to_show = [book for book in books if year is None or year <= book.year][:limit]
    for book in books_to_show:
        print(book)


def load_data():
    """Loads the data from the html file

    Creates the soup object and processes it to extract the information
    required to create the Book class objects and returns a sorted list
    of Book objects.

    Books should be sorted by rating, year, title, and then by author's
    last name. After the books have been sorted, the rank of each book
    should be updated to indicate this new sorting order.The Book object
    with the highest rating should be first and go down from there.
    """
    def transform_name(raw_name):
        name_split = raw_name.split(' ')
        last_name = name_split[-1]
        remaining_names = ' '.join(name_split[:len(name_split)-1])
        return f'{last_name}, {remaining_names}'

    soup = BeautifulSoup(open(html_file), "html.parser")
    books = soup.find(class_='books').find_all(class_='book')
    parsed_books = []
    for book in books:
        title = book.find(class_='book-title').find(class_='main').text
        if 'python' in title.lower():
            try:
                author = transform_name(book.find(class_='authors').find('a').text)
                year = int(book.find(class_='date').text[2:])
                rank = int(book.find(class_='rank').text)
                rating = float(book.find(class_='our-rating').text)
                parsed_book = Book(title, author, year, rank, rating)
                parsed_books.append(parsed_book)
            except AttributeError:
                pass
    author_sorted_books = sorted(parsed_books, key=attrgetter('author'))
    sorted_books = sorted(author_sorted_books, key=lambda book: (
        book.rating * -1,
        book.year,
        book.title.lower()
    ))
    for new_rank, book in enumerate(sorted_books):
        book.rank = new_rank + 1
    return sorted_books


def main():
    books = load_data()
    display_books(books, limit=5, year=2017)
    """If done correctly, the previous function call should display the
    output below.
    """


if __name__ == "__main__":
    main()

"""
[001] Python Tricks (2017)
      Bader, Dan 4.74
[002] Mastering Deep Learning Fundamentals with Python (2019)
      Wilson, Richard 4.7
[006] Python Programming (2019)
      Fedden, Antony Mc 4.68
[007] Python Programming (2019)
      Mining, Joseph 4.68
[009] A Smarter Way to Learn Python (2017)
      Myers, Mark 4.66
"""