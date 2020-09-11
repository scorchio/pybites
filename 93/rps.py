from random import choice

defeated_by = dict(paper='scissors',
                   rock='paper',
                   scissors='rock')
lose = '{} beats {}, you lose!'
win = '{} beats {}, you win!'
tie = 'tie!'


def _get_computer_move():
    """Randomly select a move"""
    return random.choice(['rock', 'paper', 'scissors'])


def _get_winner(computer_choice, player_choice):
    """Return above lose/win/tie strings populated with the
       appropriate values (computer vs player)"""
    if computer_choice == player_choice:
        return tie
    elif defeated_by[player_choice] == computer_choice:
        return lose.format(computer_choice, player_choice)
    return win.format(player_choice, computer_choice)


def game():
    """Game loop, receive player's choice via the generator's
       send method and get a random move from computer (_get_computer_move).
       Raise a StopIteration exception if user value received = 'q'.
       Check who wins with _get_winner and print its return output."""
    out = "Welcome to Rock Paper Scissors"
    while True:
        choice = (yield out)
        if choice not in ['q', 'rock', 'paper', 'scissors']:
            print('Invalid selection, try again!')
        elif choice == 'q':
            raise StopIteration()
        else:
            print(_get_winner(_get_computer_move(), choice))
