import re


def count_n_repetitions(text, n=1):
    """
    Counts how often characters are followed by themselves for
    n times.

    text: UTF-8 compliant input text
    n: How often character should be repeated, defaults to 1
    """
    matches = re.findall(f'(.)(?=\\1{{{n}}})', text, flags=re.MULTILINE + re.DOTALL)
    return len(matches)

def count_n_reps_or_n_chars_following(text, n=1, char=""):
    """
    Counts how often characters are repeated for n times, or
    followed by char n times.

    text: UTF-8 compliant input text
    n: How often character should be repeated, defaults to 1
    char: Character which also counts if repeated n times
    """
    if char == "":
        return count_n_repetitions(text, n)
    char = re.escape(char)
    regex = f'(.)(?=(\\1{{{n}}}|{char}{{{n}}}))'
    matches = re.findall(regex, text, flags=re.MULTILINE + re.DOTALL)
    return len(matches)

def check_surrounding_chars(text, surrounding_chars):
    """
    Count the number of times a character is surrounded by
    characters from the surrounding_chars list.

    text: UTF-8 compliant input text
    surrounding_chars: List of characters
    """
    surrounding_chars = ''.join(re.escape(char) for char in surrounding_chars)
    regex = f'(?<=[{surrounding_chars}]).(?=[{surrounding_chars}])'
    matches = re.findall(regex, text, flags=re.MULTILINE + re.DOTALL)
    return len(matches)