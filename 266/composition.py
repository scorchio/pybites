from abc import ABC, abstractmethod
from collections import namedtuple
from dataclasses import dataclass
from datetime import date
from os import getenv
from pathlib import Path
from typing import Any, List, Optional
from urllib.request import urlretrieve

from bs4 import BeautifulSoup as Soup  # type: ignore

TMP = getenv("TMP", "/tmp")
TODAY = date.today()
Candidate = namedtuple("Candidate", "name votes")
LeaderBoard = namedtuple(
    "LeaderBoard", "Candidate Average Delegates Contributions Coverage"
)
Poll = namedtuple(
    "Poll",
    "Poll Date Sample Sanders Biden Gabbard Spread",
)


class File:
    """File represents a filesystem path.

    Variables:
        name: str -- The filename that will be created on the filesystem.
        path: Path -- Path object created from the name passed in.

    Methods:
        [property]
        data: -> Optional[str] -- If the file exists, it returns its contents.
            If it does not exists, it returns None.
    """
    def __init__(self, name: str):
        self.name = name
        self.path = Path(f'{TMP}/{TODAY}_{self.name}')

    @property
    def data(self) -> Optional[str]:
        if not self.path.exists():
            return None
        
        with open(self.path) as f:
            contents = f.read()

        return contents

@dataclass
class Web:
    """Web object.

    Web is an object that downloads the page from the url that is passed
    to it and stores it in the File instance that is passed to it. If the
    File already exists, it just reads the file, otherwise it downloads it
    and stores it in File.

    Variables:
        url: str -- The url of the web page.
        file: File -- The File object to store the page data into.

    Methods:
        [property]
        data: -> Optional[str] -- Reads the text from File or retrieves it from the
            web if it does not exists.

        [property]
        soup: -> Soup -- Parses the data from File and turns it into a BeautifulSoup
            object.
    """
    url: str
    file: File

    @property
    def data(self) -> Optional[str]:
        """Reads the data from the File object.

        First it checks if the File object has any data. If it doesn't, it retrieves
        it and saves it to the File. Once the. It then reads it from the File and
        returns it.

        Returns:
            Optional[str] -- The string data from the File object.
        """
        if not self.file.data:
            urlretrieve(self.url, self.file.path)
        
        return self.file.data

    @property
    def soup(self) -> Soup:
        """Converts string data from File into a BeautifulSoup object.

        Returns:
            Soup -- BeautifulSoup object created from the File.
        """
        data = self.data
        return Soup(data, 'html.parser')


class Site(ABC):
    """Site Abstract Base Class.

    Defines the structure for the objects based on this class and defines the interfaces
    that should implemented in order to work properly.

    Variables:
        web: Web -- The web object stores the information needed to process
            the data.

    Methods:
        find_table: -> str -- Parses the Web object for table elements and
            returns the first one that it finds unless an integer representing
            the required table is passed.

        [abstractmethod]
        parse_rows: -> Union[List[LeaderBoard], List[Poll]] -- Parses a BeautifulSoup
            table element and returns the text found in the td elements as
            namedtuples.

        [abstractmethod]
        polls: -> Union[List[LeaderBoard], List[Poll]] -- Does the parsing of the table
            and rows for you. It takes the table index number if given, otherwise
            parses table 0.

        [abstractmethod]
        stats: -- Formats the results from polls into a more user friendly
            representation.
    """
    pass

    def find_table(self, loc: int = 0) -> str:
        """Finds the table elements from the Soup object

        Keyword Arguments:
            loc {int} -- Parses the Web object for table elements and
                returns the first one that it finds unless an integer representing
                the required table is passed. (default: {0})

        Returns:
            str -- The html table
        """
        tables = self.web.soup.find_all('table')
        return tables[loc]

    @abstractmethod
    def parse_rows(self, table: Soup) -> List[Any]:
        """Abstract Method
        
        Parses the row data from the html table.

        Arguments:
            table {Soup} -- Parses a BeautifulSoup table element and
                returns the text found in the td elements as NamedTuple.

        Returns:
            List[NamedTuple] -- List of NamedTuple that were created from the
                table data.
        """
        pass

    @abstractmethod
    def polls(self, table: int = 0) -> List[Any]:
        """Abstract Method

        Parses the data

        The find_table and parse_rows methods are called for you and the table index
        that is passed to it is used to get the correct table from the soup object.

        Keyword Arguments:
            table {int} -- Does the parsing of the table and rows for you.
                It takes the table index number if given, otherwise parses table 0.
                (default: {0})

        Returns:
            List[NamedTuple] -- List of NamedTuple that were created from the
                table data.
        """
        pass

    @abstractmethod
    def stats(self, loc: int = 0):
        """Abstract Method
        
        Produces the stats from the polls.

        Keyword Arguments:
            loc {int} -- Formats the results from polls into a more user friendly
            representation.
        """
        pass


@dataclass
class RealClearPolitics(Site):
    """RealClearPolitics object.

    RealClearPolitics is a custom class to parse a Web instance from the
    realclearpolitics website.

    Variables:
        web: Web -- The web object stores the information needed to process
            the data.

    Methods:
        find_table: -> str -- Parses the Web object for table elements and
            returns the first one that it finds unless an integer representing
            the required table is passed.

        parse_rows: -> List[Poll] -- Parses a BeautifulSoup table element and
            returns the text found in the td elements as Poll namedtuples.

        polls: -> List[Poll] -- Does the parsing of the table and rows for you.
            It takes the table index number if given, otherwise parses table 0.

        stats: -- Formats the results from polls into a more user friendly
            representation:

            Example:

            RealClearPolitics
            =================
                Biden: 214.0
              Sanders: 142.0
              Gabbard: 6.0

    """
    web: Web

    def parse_rows(self, table: Soup) -> List[Poll]:
        """Parses the row data from the html table.

        Arguments:
            table {Soup} -- Parses a BeautifulSoup table element and
                returns the text found in the td elements as Poll namedtuples.

        Returns:
            List[Poll] -- List of Poll namedtuples that were created from the
                table data.
        """
        def _convert_td(td):
            try:
                return float(td)
            except ValueError:
                return td

        def _poll_from_row(header_cells, tr):
            data = [_convert_td(td.text) for td in tr]
            poll_dict = {header_cells[i]: data[i] for i in range(len(data))}
            return Poll(**poll_dict)

        header_cells = [cell.text.strip() for cell in table.find_all('th')]
        polls = [_poll_from_row(header_cells, tr) for tr in table.find_all('tr')[2:]]
        return polls

    def polls(self, table: int = 0) -> List[Poll]:
        """Parses the data

        The find_table and parse_rows methods are called for you and the table index
        that is passed to it is used to get the correct table from the soup object.

        Keyword Arguments:
            table {int} -- Does the parsing of the table and rows for you.
                It takes the table index number if given, otherwise parses table 0.
                (default: {0})

        Returns:
            List[Poll] -- List of Poll namedtuples that were created from the
                table data.
        """
        table = self.find_table(table)
        polls = self.parse_rows(table)
        return polls

    def stats(self, loc: int = 0):
        """Produces the stats from the polls.

        Keyword Arguments:
            loc {int} -- Formats the results from polls into a more user friendly
            representation.
        """
        polls = self.polls(loc)
        biden = sum([poll.Biden if isinstance(poll.Biden, float) else 0 for poll in polls])
        sanders = sum([poll.Sanders if isinstance(poll.Sanders, float) else 0 for poll in polls])
        gabbard = sum([poll.Gabbard if isinstance(poll.Gabbard, float) else 0 for poll in polls])

        output = ("\n"
                  "RealClearPolitics\n"
                  "=================\n"
                  f"    Biden: {biden}\n"
                  f"  Sanders: {sanders}\n"
                  f"  Gabbard: {gabbard}"
                  "\n")

        print(output)


@dataclass
class NYTimes(Site):
    """NYTimes object.

    NYTimes is a custom class to parse a Web instance from the nytimes website.

    Variables:
        web: Web -- The web object stores the information needed to process
            the data.

    Methods:
        find_table: -> str -- Parses the Web object for table elements and
            returns the first one that it finds unless an integer representing
            the required table is passed.

        parse_rows: -> List[LeaderBoard] -- Parses a BeautifulSoup table element and
            returns the text found in the td elements as LeaderBoard namedtuples.

        polls: -> List[LeaderBoard] -- Does the parsing of the table and rows for you.
            It takes the table index number if given, otherwise parses table 0.

        stats: -- Formats the results from polls into a more user friendly
            representation:

            Example:

            NYTimes
            =================================

                               Pete Buttigieg
            ---------------------------------
            National Polling Average: 10%
                   Pledged Delegates: 25
            Individual Contributions: $76.2m
                Weekly News Coverage: 3

    """

    web: Web

    def parse_rows(self, table: Soup) -> List[LeaderBoard]:
        """Parses the row data from the html table.

        Arguments:
            table {Soup} -- Parses a BeautifulSoup table element and
                returns the text found in the td elements as LeaderBoard namedtuples.

        Returns:
            List[LeaderBoard] -- List of LeaderBoard namedtuples that were created from
            the table data.
        """

        def _leaderboard_from_row(tr):
            data = []
            name = tr.find(class_='g-desktop')
            if not name:
                return None
            data.append(name.text.strip())
            data.extend([td.text.strip() for td in tr.find_all('td')[1:]])
            if len(data) < 4:
                return None
            data[2] = int(data[2])
            data[4] = int(data[4].replace('#', ''))
            return LeaderBoard(*data)

        leaderboards = [
            _leaderboard_from_row(tr) 
            for tr in table.find_all('tr')[1:] 
            if _leaderboard_from_row(tr) is not None
        ]
        return leaderboards

    def polls(self, table: int = 0) -> List[LeaderBoard]:
        """Parses the data

        The find_table and parse_rows methods are called for you and the table index
        that is passed to it is used to get the correct table from the soup object.

        Keyword Arguments:
            table {int} -- Does the parsing of the table and rows for you.
                It takes the table index number if given, otherwise parses table 0.
                (default: {0})

        Returns:
            List[LeaderBoard] -- List of LeaderBoard namedtuples that were created from
                the table data.
        """
        table = self.find_table(table)
        polls = self.parse_rows(table)
        return polls

    def stats(self, loc: int = 0):
        """Produces the stats from the polls.

        Keyword Arguments:
            loc {int} -- Formats the results from polls into a more user friendly
            representation.

            NYTimes
            =================================

                            Pete Buttigieg
            ---------------------------------
            National Polling Average: 10%
                Pledged Delegates: 25
            Individual Contributions: $76.2m
                Weekly News Coverage: 3
        """
        leaderboard = self.polls(loc)
        for entry in leaderboard:
            print ("\n"
                   "NYTimes\n"
                   "=================================\n"
                   f"{entry.Candidate:>33}\n"
                   "---------------------------------\n"
                   f"National Polling Average: {entry.Average}\n"
                   f"       Pledged Delegates: {entry.Delegates}\n"
                   f"Individual Contributions: {entry.Contributions}\n"
                   f"    Weekly News Coverage: {entry.Coverage}\n"
                   "\n")


def gather_data():
    rcp_file = File("realclearpolitics.html")
    rcp_url = (
        "https://bites-data.s3.us-east-2.amazonaws.com/2020-03-10_realclearpolitics.html"
    )
    rcp_web = Web(rcp_url, rcp_file)
    rcp = RealClearPolitics(rcp_web)
    rcp.stats(3)

    nyt_file = File("nytimes.html")
    nyt_url = (
        "https://bites-data.s3.us-east-2.amazonaws.com/2020-03-10_nytimes.html"
    )
    nyt_web = Web(nyt_url, nyt_file)
    nyt = NYTimes(nyt_web)
    nyt.stats()


if __name__ == "__main__":
    gather_data()