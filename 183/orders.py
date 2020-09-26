import os
from urllib.request import urlretrieve

import pandas as pd
import numpy as np

TMP = os.getenv("TMP", "/tmp")
EXCEL = os.path.join(TMP, 'order_data.xlsx')
if not os.path.isfile(EXCEL):
    urlretrieve(
        'https://bites-data.s3.us-east-2.amazonaws.com/order_data.xlsx',
        EXCEL
    )


def load_excel_into_dataframe(excel=EXCEL):
    """Load the SalesOrders sheet of the excel book (EXCEL variable)
       into a Pandas DataFrame and return it to the caller"""
    return pd.read_excel(excel, sheet_name='SalesOrders')


def get_year_region_breakdown(df):
    """Group the DataFrame by year and region, summing the Total
       column. You probably need to make an extra column for
       year, return the new df as shown in the Bite description"""
    df['Year'] = df['OrderDate'].apply(lambda x: int(str(x).split('-')[0]))
    return df.groupby(['Year', 'Region']).agg({'Total': [np.sum]})


def get_best_sales_rep(df):
    """Return a tuple of the name of the sales rep and
       the total of his/her sales"""
    best_sales_df = df.groupby('Rep').sum('Total')
    best = best_sales_df[best_sales_df.Total == best_sales_df.Total.max()]
    return best.index.values[0], best['Total'].values[0]


def get_most_sold_item(df):
    """Return a tuple of the name of the most sold item
       and the number of units sold"""
    best_df = df.groupby('Item').sum('Units')
    best = best_df[best_df.Total == best_df.Total.max()]
    return best.index.values[0], best['Units'].values[0]
