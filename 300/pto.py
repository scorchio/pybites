from dateutil.rrule import DAILY, FR, MO, WEEKLY, rrule
from datetime import date, datetime, timedelta
from pprint import pprint
import calendar


ERROR_MSG = (
    "Unambiguous value passed, please specify either start_month or show_workdays"
)
FEDERAL_HOLIDAYS = (
    date(2020, 9, 7),
    date(2020, 10, 12),
    date(2020, 11, 11),
    date(2020, 11, 26),
    date(2020, 12, 25),
)
WFH = (calendar.TUESDAY, calendar.WEDNESDAY)
WEEKENDS = (calendar.SATURDAY, calendar.SUNDAY)
AT_HOME = WFH + WEEKENDS


def four_day_weekends(
        start_month: int = 8,
        paid_time_off: int = 200,
        year: int = 2020,
        show_workdays: bool = False
    ) -> None:
    """Generates four day weekend report

    The four day weekends are calculated from the start_month through the end of the year
    along with the number of work days for the same time period. The reports takes into
    account any holidays that might fall within that time period and days designated as
    working from home (WFH).

    If show_workdays is set to True, a report with the work days is generated instead of
    the four day weekend dates.

    Args:
        start_month (int, optional): Month to start. Defaults to 8.
        paid_time_off (int, optional): Paid vacation days
        year (int, optional): Year to calculate, defaults to current year
        show_workdays (bool, optional): Enables work day report. Defaults to False.

    Raises:
        ValueError: ERROR_MSG
    """
    if isinstance(start_month, bool):
        raise ValueError(ERROR_MSG)

    candidates = _generate_staycation_candidates(year, start_month)
    weekends_without_federal_holidays = _filter_federal_holidays(candidates)
    base = _get_report_base(year, start_month, paid_time_off, weekends_without_federal_holidays)

    if show_workdays:
        print(_generate_work_day_report(base))
    else:
        print(_generate_four_day_weekend_report(base))


def _get_report_base(year, start_month, paid_time_off, weekends_without_federal_holidays):
    weekends = []
    staycation_days = []
    pto_days_count = paid_time_off // 8
    last_chance_was_displayed = False
    start_date = datetime(year, start_month, 1)
    for start, end in reversed(weekends_without_federal_holidays):
        staycation_days.extend([end, start])
        last_chance = len(staycation_days) > pto_days_count and not last_chance_was_displayed
        weekends.append((start, end, last_chance))
        if last_chance:
            last_chance_was_displayed = True

    staycation_days.reverse()
    weekends.reverse()
    balance_days = abs(pto_days_count - len(staycation_days))

    workdays = _generate_work_days(year, start_month, staycation_days)

    base = {
        'pto_days_count': pto_days_count,
        'balance_days_count': balance_days,
        'workdays': workdays,
        'weekends': weekends,
    }
    return base


def _generate_work_days(year, start_month, staycation_days):
    start_date = datetime(year, start_month, 1)
    last_date = datetime(year, 12, 31)
    days = rrule(freq=DAILY, dtstart=start_date, until=last_date)
    workdays = []
    for day in days:
        is_workday = (
            day not in staycation_days and
            day.weekday() not in AT_HOME and
            day.date() not in FEDERAL_HOLIDAYS
        )
        if is_workday:
            workdays.append(day)
        
    return workdays


def _generate_staycation_candidates(year, start_month):
    friday_to_monday = timedelta(days=3)
    start_date = datetime(year, start_month, 1)
    last_date = datetime(year, 12, 31)
    fridays = rrule(freq=WEEKLY, byweekday=FR, 
                    dtstart=start_date, until=last_date)
    mondays = rrule(freq=WEEKLY, byweekday=MO, 
                    dtstart=start_date + friday_to_monday, until=last_date + friday_to_monday)
    candidates = list(zip(fridays, mondays))
    return candidates


def _filter_federal_holidays(candidates):
    filtered = []
    for friday, monday in candidates:
        is_federal_holiday = (
            friday.date() in FEDERAL_HOLIDAYS # or
            # monday.date() in FEDERAL_HOLIDAYS
        )
        if not is_federal_holiday:
            filtered.append((friday, monday))
        # else:
           # print(f'Between {friday} and {monday}, there is a holiday -> not a staycation')
    return filtered


def _generate_four_day_weekend_report(results):
    results['pto_count'] = results['pto_days_count'] * 8
    results['balance_count'] = results['balance_days_count'] * -8
    output = _get_four_day_weekend_output(results)
    return output


def _get_four_day_weekend_output(results):
    line_width = 24
    weekends_count = len(results['weekends'])
    header_line_text = f'{weekends_count} Four-Day Weekends'
    header_line = f'{header_line_text:^{line_width}}'
    separator = '=' * line_width 
    pto_line = f'{"PTO: ":>9} {results["pto_count"]:>3} ({results["pto_days_count"]} days)'
    balance_line = f'{"BALANCE: ":>9} {results["balance_count"]:>2} ({results["balance_days_count"]} days)'   
    output_lines = [header_line, separator, pto_line, balance_line, '']
    output_lines.extend(_get_weekend_lines(results['weekends']))
    output = '\n'.join(output_lines)
    return output


def _get_weekend_lines(weekends):
    weekend_lines = []
    for start, end, is_last_chance in weekends:
        start_date = start.date()
        end_date = end.date()
        line = f'{start_date} - {end_date} *' if is_last_chance else f'{start_date} - {end_date}'
        weekend_lines.append(line)
    return weekend_lines


def _generate_work_day_report(base):
    results = {
        'remaining_work_days': len(base['workdays']),
        'days': base['workdays'],
    }
    results['remaining_work'] = results['remaining_work_days'] * 8
    output = _get_work_day_output(results)
    return output


def _get_work_day_output(results):
    header_line = f'Remaining work days: {results["remaining_work"]} ({results["remaining_work_days"]} days)'
    output_lines = [header_line]
    days = [str(day.date()) for day in results['days']]
    output_lines.extend(days)
    output = '\n'.join(output_lines)
    return output


if __name__ == "__main__":
    four_day_weekends(show_workdays=True)
