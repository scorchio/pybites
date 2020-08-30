scores = [10, 50, 100, 175, 250, 400, 600, 800, 1000]
ranks = 'white yellow orange green blue brown black paneled red'.split()
BELTS = dict(zip(scores, ranks))


class NinjaBelt:

    def __init__(self, score=0):
        self._score = score
        self._last_earned_belt = None

    def _get_belt(self, new_score):
        belt_index = -1
        for i, score in enumerate(scores):
            if new_score >= score:
                belt_index = i
        if belt_index == -1:
            return None
        return ranks[belt_index]

    def _get_score(self):
        return self._score

    def _set_score(self, new_score):
        if not isinstance(new_score, int):
            raise ValueError("Score takes an int")
        if new_score < self._score:
            raise ValueError("Cannot lower score")

        self._score = new_score
        new_belt = self._get_belt(new_score)
        if new_belt != self._last_earned_belt:
            print(f'Congrats, you earned {self._score} points obtaining the PyBites Ninja {new_belt.title()} Belt')
        else:
            print(f'Set new score to {self._score}')
        self._last_earned_belt = new_belt       

    score = property(_get_score, _set_score)