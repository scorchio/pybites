from dataclasses import dataclass, field
from typing import List, Tuple
import heapq

bites: List[int] = [283, 282, 281, 263, 255, 230, 216, 204, 197, 196, 195]
names: List[str] = [
    "snow",
    "natalia",
    "alex",
    "maquina",
    "maria",
    "tim",
    "kenneth",
    "fred",
    "james",
    "sara",
    "sam",
]


@dataclass
class Ninja:
    """
    The Ninja class will have the following features:

    string: name
    integer: bites
    support <, >, and ==, based on bites
    print out in the following format: [469] bob
    """
    name: str
    bites: int

    def __str__(self):
        return f'[{self.bites}] {self.name}'

    def __eq__(self, other):
        return self.bites == other.bites

    def __lt__(self, other):
        return self.bites < other.bites

    def __gt__(self, other):
        return self.bites > other.bites


@dataclass
class Rankings:
    """
    The Rankings class will have the following features:

    method: add() that adds a Ninja object to the rankings
    method: dump() that removes/dumps the lowest ranking Ninja from Rankings
    method: highest() returns the highest ranking Ninja, but it takes an optional
            count parameter indicating how many of the highest ranking Ninjas to return
    method: lowest(), the same as highest but returns the lowest ranking Ninjas, also
            supports an optional count parameter
    returns how many Ninjas are in Rankings when len() is called on it
    method: pair_up(), pairs up study partners, takes an optional count
            parameter indicating how many Ninjas to pair up
    returns List containing tuples of the paired up Ninja objects
    """
    heap: List[Ninja] = field(default_factory=list)

    def __len__(self):
        return len(self.heap)

    def add(self, new_ninja: Ninja) -> None:
        if new_ninja not in self.heap:
            heapq.heappush(self.heap, new_ninja)

    def dump(self) -> Ninja:
        return heapq.heappop(self.heap)

    def lowest(self, count: int = 1) -> List[Ninja]:
        return heapq.nsmallest(count, self.heap)

    def highest(self, count: int = 1) -> List[Ninja]:
        return heapq.nlargest(count, self.heap)

    def pair_up(self, count: int = 3) -> List[Tuple[Ninja, Ninja]]:
        pairings = list(zip(
            heapq.nlargest(count, self.heap),
            heapq.nsmallest(count, self.heap)
        ))
        return pairings