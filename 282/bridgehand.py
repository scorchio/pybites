from collections import namedtuple
from collections.abc import Sequence as SequenceType
from enum import Enum
from typing import Sequence

Suit = Enum("Suit", list("SHDC"))
Rank = Enum("Rank", list("AKQJT98765432"))
Card = namedtuple("Card", ["suit", "rank"])

HCP = {Rank.A: 4, Rank.K: 3, Rank.Q: 2, Rank.J: 1}
SSP = {2: 1, 1: 2, 0: 3}  # cards in a suit -> short suit points


class BridgeHand:
    def __init__(self, cards: Sequence[Card]):
        """
        Process and store the sequence of Card objects passed in input.
        Raise TypeError if not a sequence
        Raise ValueError if any element of the sequence is not an instance
        of Card, or if the number of elements is not 13
        """
        if not isinstance(cards, SequenceType):
            raise TypeError('Cards must be a sequence')

        if not len(cards) == 13:
            raise ValueError('Number of cards must be 13')

        self.hand = {
            Suit.S: [],
            Suit.H: [],
            Suit.D: [],
            Suit.C: [],
        }
        for card in cards:
            if not isinstance(card, Card):
                raise ValueError('All items in cards must be a Card type')
            self.hand[card.suit].append(card)


    def __str__(self) -> str:
        """
        Return a string representing this hand, in the following format:
        "S:AK3 H:T987 D:KJ98 C:QJ"
        List the suits in SHDC order, and the cards within each suit in
        AKQJT..2 order.
        Separate the suit symbol from its cards with a colon, and
        the suits with a single space.
        Note that a "10" should be represented with a capital 'T'
        """
        output_parts = []
        for suit, cards in self.hand.items():
            if len(cards) == 0:
                continue
            
            sorted_cards = list(sorted(cards, key=lambda card: card.rank.value))
            card_values = ''.join([card.rank.name for card in sorted_cards])
            output_parts.append(f'{suit.name}:{card_values}')
        return ' '.join(output_parts)

    @property
    def hcp(self) -> int:
        """ Return the number of high card points contained in this hand """
        points = 0
        for cards in self.hand.values():
            points += sum([HCP.get(card.rank, 0) for card in cards])
        return points

    def _num_of_suits_with_n_cards(self, n: int) -> int:
        n_count = [1 if len(cards) == n else 0 for cards in self.hand.values()]
        return sum(n_count)

    @property
    def doubletons(self) -> int:
        """ Return the number of doubletons contained in this hand """
        return self._num_of_suits_with_n_cards(2)

    @property
    def singletons(self) -> int:
        """ Return the number of singletons contained in this hand """
        return self._num_of_suits_with_n_cards(1)

    @property
    def voids(self) -> int:
        """ Return the number of voids (missing suits) contained in
            this hand
        """
        return self._num_of_suits_with_n_cards(0)

    @property
    def ssp(self) -> int:
        """ Return the number of short suit points in this hand.
            Doubletons are worth one point, singletons two points,
            voids 3 points
        """
        points = 0
        for count, point in SSP.items():
            points += self._num_of_suits_with_n_cards(count)*point
        return points

    @property
    def total_points(self) -> int:
        """ Return the total points (hcp and ssp) contained in this hand """
        return self.hcp + self.ssp

    @property
    def ltc(self) -> int:
        """ Return the losing trick count for this hand - see bite description
            for the procedure
        """
        not_losers = [Rank.A, Rank.K, Rank.Q]
        points = 0
        for cards in self.hand.values():
            not_losers_to_check = not_losers[:len(cards)]
            count_in_suit = 0
            cards_rank = [card.rank for card in cards]
            for rank in not_losers_to_check:
                if rank in cards_rank:
                    count_in_suit += 1
            points += min(3, len(cards)) - count_in_suit
        return points
