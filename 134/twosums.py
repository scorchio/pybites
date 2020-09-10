from itertools import combinations

def two_sums(numbers, target):
    """Finds the indexes of the two numbers that add up to target.

    :param numbers: list - random unique numbers
    :param target: int - sum of two values from numbers list
    :return: tuple - (index1, index2) or None
    """
    possible_matches = [
        pair for pair in combinations(enumerate(numbers), 2)
        if pair[0][1]+pair[1][1] == target and pair[0][0] < pair[1][0]
    ]
    if len(possible_matches) == 0:
        return None

    match = min(possible_matches, key=lambda x: x[0][1])
    return (match[0][0], match[1][0])
