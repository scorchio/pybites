from datetime import datetime
from operator import itemgetter
from pathlib import Path
import json

SCORES = [10, 50, 100, 175, 250, 400, 600, 800, 1000]
BELTS = ('white yellow orange green blue brown black '
         'paneled red').split()
TMP = Path('/tmp')


def get_belts(path: str) -> dict:
    """Parsed the passed in json data:
       {"date":"5/1/2019","score":1},
       {"date":"9/13/2018","score":3},
       {"date":"10/25/2019","score":1},

       Loop through the scores in chronological order,
       determining when belts were achieved (use SCORES
       and BELTS).

       Return a dict with keys = belts, and values =
       readable dates, example entry:
       'yellow': 'January 25, 2018'
    """
    with open(path) as json_file:
        data = json.load(json_file)
    for entry in data:
        entry['date'] = datetime.strptime(entry['date'], '%m/%d/%Y').date()
    data.sort(key=itemgetter('date'))
    score = 0
    belt_idx = 0
    belts_achieved = {}
    for entry in data:
        score += entry['score']
        if belt_idx < len(SCORES) and score >= SCORES[belt_idx]:
            belts_achieved[BELTS[belt_idx]] = entry['date'].strftime('%B %d, %Y')
            belt_idx += 1
    return belts_achieved