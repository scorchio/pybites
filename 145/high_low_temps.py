from collections import namedtuple
from datetime import date

import numpy as np
import pandas as pd

DATA_FILE = "https://bites-data.s3.us-east-2.amazonaws.com/weather-ann-arbor.csv"
STATION = namedtuple("Station", "ID Date Value")


def high_low_record_breakers_for_2015():
    def _date_to_md(value):
        d = date.fromisoformat(value)
        return f'{d.month:02}-{d.day:02}'

    def _date_to_year(value):
        return int(value.split('-')[0])
    
    df = pd.read_csv(DATA_FILE)
    df['date_str'] = df['Date'].apply(_date_to_md)
    df['year'] = df['Date'].apply(_date_to_year)
    
    minmax = df[df.year < 2015].groupby(['ID', 'date_str']).agg({'Data_Value': [np.min, np.max]})
    temperatures_2015 = df[df.year == 2015].groupby(['ID', 'date_str']).agg({'Data_Value': [np.min, np.max]})

    record_min = None
    record_max = None
    for idx, df in temperatures_2015.groupby(level=[0, 1]):
        min_temp_2015, max_temp_2015 = df.loc[idx]['Data_Value']
        min_temp, max_temp = minmax.loc[idx]['Data_Value']
        if min_temp_2015 < min_temp:
            if record_min is None or min_temp_2015 < record_min.Value * 10:
                record_min = STATION(
                    ID=idx[0], 
                    Date=date.fromisoformat(f'2015-{idx[1]}'), 
                    Value=min_temp_2015 / 10
                )
        if max_temp_2015 > max_temp:
            if record_max is None or max_temp_2015 > record_max.Value * 10:
                record_max = STATION(
                    ID=idx[0], 
                    Date=date.fromisoformat(f'2015-{idx[1]}'),
                    Value=max_temp_2015 / 10
                )

    return record_max, record_min
