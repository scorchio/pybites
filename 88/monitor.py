from collections import Counter
from contextlib import contextmanager
from datetime import date
from time import time

OPERATION_THRESHOLD_IN_SECONDS = 2.2
ALERT_THRESHOLD = 3
ALERT_MSG = 'ALERT: suffering performance hit today'

violations = Counter()


def get_today():
    """Making it easier to test/mock"""
    return date.today()


@contextmanager
def timeit():
    try:
        start = time()
        yield
    finally:
        end = time()
        spent = end - start
        if spent >= OPERATION_THRESHOLD_IN_SECONDS:
            today = get_today()
            violations[today] += 1
            if violations[today] >= ALERT_THRESHOLD:
                print(ALERT_MSG)
