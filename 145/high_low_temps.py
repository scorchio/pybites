from collections import namedtuple
from datetime import date

import numpy as np
import pandas as pd

DATA_FILE = "https://bites-data.s3.us-east-2.amazonaws.com/weather-ann-arbor.csv"
STATION = namedtuple("Station", "ID Date Value")


def high_low_record_breakers_for_2015():
    def _date_to_monthday(value):
        d = date.fromisoformat(value)
        return f'{d.month}-{d.day}'

    df = pd.read_csv(DATA_FILE)
    df['monthday'] = df['Date'].apply(_date_to_monthday)
    df['min'] = df.groupby(['ID', 'monthday'])['Data_Value'].min()
    df['max'] = df.groupby(['ID', 'monthday'])['Data_Value'].max()
    pass

high_low_record_breakers_for_2015()