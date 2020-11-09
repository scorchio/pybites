import calendar
from datetime import date


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
    if show_workdays:
        print(_generate_work_day_report())
    else:
        print(_generate_four_day_weekend_report())


def _generate_four_day_weekend_report():
    results = {
        'four_day_weekends_count': 18,
        'pto_count': 200,
        'pto_days_count': 25,
        'balance_count': -88,
        'balance_days_count': 11,
        'weekends': [
            ('2020-08-07', '2020-08-10', False),
            ('2020-09-18', '2020-09-21', True),
            ('2020-12-18', '2020-12-21', False),
        ],
    }
    output = _get_four_day_weekend_output(results)
    return output


def _get_four_day_weekend_output(results):
    line_width = 24
    header_line_text = f'{results["four_day_weekends_count"]} Four-Day Weekends'
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
        line = f'{start} - {end} *' if is_last_chance else f'{start} - {end}'
        weekend_lines.append(line)
    return weekend_lines


def _generate_work_day_report():
    results = {
        'remaining_work': 184,
        'remaining_work_days': 23,
        'days': ['2020-08-03', '2020-08-06'],
    }
    output = _get_work_day_output(results)
    return output


def _get_work_day_output(results):
    header_line = f'Remaining work days: {results["remaining_work"]} ({results["remaining_work_days"]} days)'
    output_lines = [header_line]
    output_lines.extend(results['days'])
    output = '\n'.join(output_lines)
    return output


if __name__ == "__main__":
    four_day_weekends(show_workdays=True)
