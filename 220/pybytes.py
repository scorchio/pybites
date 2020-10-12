from collections import namedtuple, Counter
from operator import itemgetter
from typing import NamedTuple
import re

import feedparser

SPECIAL_GUEST = 'Special guest'

# using _ as min/max are builtins
Duration = namedtuple('Duration', 'avg max_ min_')

# static copy, original: https://pythonbytes.fm/episodes/rss
URL = 'https://bites-data.s3.us-east-2.amazonaws.com/python_bytes'
IGNORE_DOMAINS = {'https://pythonbytes.fm', 'http://pythonbytes.fm',
                  'https://twitter.com', 'https://training.talkpython.fm',
                  'https://talkpython.fm', 'http://testandcode.com'}


class PythonBytes:

    def __init__(self, url=URL):
        """Load the feed url into self.entries using the feedparser module."""
        self.entries = feedparser.parse(url).entries

    def get_episode_numbers_for_mentioned_domain(self, domain: str) -> list:
        """Return a list of episode IDs (itunes_episode attribute) of the
           episodes the pass in domain was mentioned in.
        """
        mentions = []
        for entry in self.entries:
            if domain in entry.summary:
                mentions.append(entry.itunes_episode)
        return mentions

    def get_most_mentioned_domain_names(self, n: int = 15) -> list:
        """Get the most mentioned domain domains. We match a domain using
           regex: "https?://[^/]+" - make sure you only count a domain once per
           episode and ignore domains in IGNORE_DOMAINS.
           Return a list of (domain, count) tuples (use Counter).
        """
        domain_counter = Counter()
        for entry in self.entries:
            domains = set()
            matches = re.findall(r'https?://[^/]+', entry.summary)
            if matches:
                for match in matches:
                    if match not in IGNORE_DOMAINS:
                        domains.add(match)
                domain_counter.update(domains)
        result = domain_counter.most_common(n)
        return result

    def number_episodes_with_special_guest(self) -> int:
        """Return the number of episodes that had one of more special guests
           featured (use SPECIAL_GUEST).
        """
        ep_with_guest_count = sum(1 for entry in self.entries if SPECIAL_GUEST in entry.summary)
        return ep_with_guest_count

    def get_average_duration_episode_in_seconds(self) -> NamedTuple:
        """Return the average duration in seconds of a Python Bytes episode, as
           well as the shortest and longest episode in hh:mm:ss notation.
           Return the results using the Duration namedtuple.
        """
        def duration_secs_from_str(duration_str):
            split = duration_str.split(':')
            return int(split[0]) * 3600 + int(split[1]) * 60 + int(split[2])

        duration_seconds = [
            (duration_secs_from_str(entry.itunes_duration), entry.itunes_duration) 
            for entry in self.entries
        ]
        min_ = min(duration_seconds, key=itemgetter(0))[1]
        max_ = max(duration_seconds, key=itemgetter(0))[1]
        avg = sum([x[0] for x in duration_seconds]) // len(duration_seconds)
        result = Duration(avg, max_, min_)
        return result
