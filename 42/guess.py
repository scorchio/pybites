import random

MAX_GUESSES = 5
START, END = 1, 20


def get_random_number():
    """Get a random number between START and END, returns int"""
    return random.randint(START, END)


class Game:
    """Number guess class, make it callable to initiate game"""

    def __init__(self):
        self._guesses, self._answer, self._win = set(), get_random_number(), False

    def guess(self):
        """Ask user for input, convert to int, raise ValueError outputting
           the following errors when applicable:
           'Please enter a number'
           'Should be a number'
           'Number not in range'
           'Already guessed'
           If all good, return the int"""

        value = input('Guess a number between 1 and 20: ')
        if not value:
            raise ValueError('Please enter a number')
        if not str(value).isdecimal():
            raise ValueError('Should be a number')
    
        number = int(value)
        if not (1 <= number <= 20):
            raise ValueError('Number not in range')

        if number in self._guesses:
            raise ValueError('Already guessed')

        self._guesses.add(number)
        return number

    def _validate_guess(self, guess):
        """Verify if guess is correct, print the following when applicable:
           {guess} is correct!
           {guess} is too low
           {guess} is too high
           Return a boolean"""
        if guess == self._answer:
            print(f'{guess} is correct!')
        elif guess < self._answer:
            print(f'{guess} is too low')
        else:
            print(f'{guess} is too high')
        return guess == self._answer

    def __call__(self):
        """Entry point / game loop, use a loop break/continue,
           see the tests for the exact win/lose messaging"""
        while len(self._guesses) < MAX_GUESSES and not self._win:
            try:
                guess = self.guess()
                if self._validate_guess(guess):
                    self._win = True
            except ValueError as err:
                print(err)
        
        if self._win:
            print(f'It took you {len(self._guesses)} guesses')
        else:
            print(f'Guessed 5 times, answer was {self._answer}')
        


if __name__ == '__main__':
    game = Game()
    game()