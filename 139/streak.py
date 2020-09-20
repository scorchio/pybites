from datetime import datetime, timedelta, date

TODAY = date(2018, 11, 12)


def extract_dates(data):
    """Extract unique dates from DB table representation as shown in Bite"""
    count_splitters = 0
    extracted = set()
    for line in data.splitlines():
        if count_splitters == 2 and '|' in line:
            date_found = date.fromisoformat(line.split('|')[1].strip())
            extracted.add(date_found)
        if '-+-' in line:
            count_splitters += 1
    return list(extracted)


def calculate_streak(dates):
    """Receives sequence (set) of dates and returns number of days
       on coding streak.

       Note that a coding streak is defined as consecutive days coded
       since yesterday, because today is not over yet, however if today
       was coded, it counts too of course.

       So as today is 12th of Nov, having dates 11th/10th/9th of Nov in
       the table makes for a 3 days coding streak.

       See the tests for more examples that will be used to pass your code.
    """
    dates_rev = sorted(dates, reverse=True)
    one_day = timedelta(days=1)
    if not dates_rev[0] == TODAY and not dates_rev[0] == TODAY - one_day:
        return 0
    
    streak = 1
    for i, date in enumerate(dates_rev[1:]):  # careful with the indexes, i is 0, the real position is 1
        if date != dates_rev[i] - one_day:
            return streak
        streak += 1
    return streak
