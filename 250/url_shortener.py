from math import floor
from string import ascii_lowercase, ascii_uppercase, digits
from typing import Dict
from urllib.parse import urlparse

CODEX: str = digits + ascii_lowercase + ascii_uppercase
BASE: int = len(CODEX)
# makeshift database record
LINKS: Dict[int, str] = {
    1: "https://pybit.es",
    45: "https://pybit.es/pages/articles.html",
    255: "http://pbreadinglist.herokuapp.com",
    600: "https://pybit.es/pages/challenges.html",
    874: "https://stackoverflow.com",
}
SITE: str = "https://pybit.es"

# error messages
INVALID = "Not a valid PyBites shortened url"
NO_RECORD = "Not a valid shortened url"


def encode(record: int) -> str:
    """Encodes an integer into Base62"""
    remainder = record % BASE
    result = CODEX[remainder]
    queue = floor(record / BASE)
    while queue:
        remainder = queue % BASE
        queue = floor(queue / BASE)
        result = CODEX[remainder] + result
    return result


def decode(short_url: str) -> int:
    """Decodes the Base62 string into a Base10 integer"""
    value = 0
    for char in short_url:
        value = value * BASE + CODEX.find(char)
    return value


def redirect(url: str) -> str:
    """Retrieves URL from shortened DB (LINKS)

    1. Check for valid domain
    2. Check if record exists
    3. Return URL stored in LINKS or proper message
    """
    parsed_url = urlparse(url)
    if SITE != f'{parsed_url.scheme}://{parsed_url.netloc}':
        return INVALID
    entry = decode(parsed_url.path[1:])
    if entry not in LINKS.keys():
        return NO_RECORD
    
    return LINKS[entry]

def shorten_url(url: str, next_record: int) -> str:
    """Shortens URL and updates the LINKS DB

    1. Encode next_record
    2. Adds url to LINKS
    3. Return shortened URL
    """
    key = encode(next_record)
    LINKS[next_record] = url
    return f'{SITE}/{key}'