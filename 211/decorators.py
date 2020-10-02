from functools import wraps

MAX_RETRIES = 3


class MaxRetriesException(Exception):
    pass


def retry(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        for i in range(MAX_RETRIES):
            try:
                return function(*args, **kwargs)
            except Exception as e:
                print(e)
        raise MaxRetriesException()
    return wrapper
