import json
import os
from collections import OrderedDict
from datetime import date, timedelta
from pathlib import Path
from typing import Dict, List
from urllib.request import urlretrieve

URL = "https://bites-data.s3.us-east-2.amazonaws.com/exchangerates.json"
TMP = Path(os.getenv("TMP", "/tmp"))
RATES_FILE = TMP / "exchangerates.json"

if not RATES_FILE.exists():
    urlretrieve(URL, RATES_FILE)


def get_all_days(start_date: date, end_date: date) -> List[date]:
    delta_days = (end_date - start_date).days
    result = [start_date + timedelta(days=date_idx) for date_idx in range(0, delta_days + 1)]
    return result


def match_daily_rates(start: date, end: date, daily_rates: dict) -> Dict[date, date]:
    source_rates = OrderedDict()
    for key in sorted(daily_rates.keys()):
        source_rates[key] = daily_rates[key]

    previous = None
    dates = {}
    for rate_date, rates in source_rates.items():
        rate_date = date.fromisoformat(rate_date)
        if previous:
            if rate_date - previous > timedelta(days=1):
                for date_between_idx in range(1, (rate_date - previous).days):
                    current_date = previous + timedelta(days=date_between_idx)
                    dates[current_date] = previous
        dates[rate_date] = rate_date
        previous = rate_date
    
    results = {
        rate_date: original_date 
        for rate_date, original_date in dates.items()
        if rate_date >= start and rate_date <= end
    }
    return results

def exchange_rates(
    start_date: str = "2020-01-01", end_date: str = "2020-09-01"
) -> Dict[date, dict]:

    with open(RATES_FILE) as json_file:
        data = json.load(json_file)

    if data['start_at'] > start_date or data['end_at'] < end_date:
        raise ValueError('Requested date range is not covered in dataset')

    previous = None
    rates_result = {}
    source_rates = OrderedDict()
    for key in sorted(data['rates'].keys()):
        source_rates[key] = data['rates'][key]

    for rate_date, rates in source_rates.items():
        rate_date = date.fromisoformat(rate_date)
        if previous:
            if rate_date - previous[0] > timedelta(days=1):
                for date_between_idx in range(1, (rate_date - previous[0]).days):
                    current_date = previous[0] + timedelta(days=date_between_idx)
                    rates_result[current_date] = {
                        'Base Date': previous[0],
                    }
                    rates_result[current_date].update(previous[1])
        rates_result[rate_date] = {
            'Base Date': rate_date,
        }
        rates_result[rate_date].update(rates)
        previous = (rate_date, rates)

    results = {
        rate_date: rates 
        for rate_date, rates in rates_result.items()
        if (
            rate_date >= date.fromisoformat(start_date) and
            rate_date <= date.fromisoformat(end_date)
        )
    }
    return results
