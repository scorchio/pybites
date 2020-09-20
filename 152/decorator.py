from functools import wraps


DEFAULT_TEXT = ('Subscribe to our blog (sidebar) to periodically get '
                'new PyBites Code Challenges (PCCs) in your inbox')
DOT = '.'


def strip_range(start, end):
    """Decorator that replaces characters of a text by dots, from 'start'
       (inclusive) to 'end' (exclusive) = like range.

        So applying this decorator on a function like this and 'text'
        being 'Hello world' it would convert it into 'Hel.. world' when
        applied like this:

        @strip_range(3, 5)
        def gen_output(text):
            return text
    """
    def _strip_range(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            retval = function(*args, **kwargs)           
            return ''.join(['.' if i in range(start, end) else c for i, c in enumerate(retval)])
        return wrapper
    return _strip_range