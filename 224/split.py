import re

def get_sentences(text):
    """Return a list of sentences as extracted from the text passed in.
       A sentence starts with [A-Z] and ends with [.?!]"""
    text_without_newlines = text.replace('\n', ' ')
    splits = re.split(r'(?<=[\.?!]) (?=[A-Z])', text_without_newlines)
    stripped_sentences = [x.strip() for x in splits]
    return stripped_sentences
