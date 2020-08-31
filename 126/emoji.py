import sys
import unicodedata


START_EMOJI_RANGE = 127744


def what_means_emoji(emoji):
    try:
        return unicodedata.name(emoji)
    except (TypeError, ValueError):
        return 'Not found'


def _make_emoji_mapping():
    return {chr(i): what_means_emoji(chr(i)) for i in range(START_EMOJI_RANGE, sys.maxunicode + 1)}


def find_emoji(term):
    """Return emojis and their texts that match (case insensitive)
       term, print matches to console"""
    term = term.upper()
    emoji_mapping = _make_emoji_mapping()
    matching_emojis = {key: value for key, value in emoji_mapping.items() if term in value}
    for emoji, name in matching_emojis.items():
        print(f'{name:<50} | {emoji}')
