# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 02:22:24 2017

@author: nmertia
"""

import pandas as pd
import pandas_datareader.data as web
import datetime
from copy import deepcopy

url = r'http://www.moneycontrol.com/stocks/marketinfo/dividends_declared/homebody.php?sel_year='
year = range(2000, 2018)

data_columns = ['Company','DivType','DivPerc','Annc. Date','Record Date','ExDate']
div = pd.DataFrame()
    
for yr in year:
    url_yr = url + str(yr)
    tables = pd.read_html(url_yr)       # Returns list of all tables on page
    
    df = tables[1]                      # Select table of interest
    div_df = df.iloc[2:]
    div_df.columns = data_columns
    
    div = div.append(div_df, ignore_index = True)

div1 = deepcopy(div)
div[['Annc. Date', 'Record Date', 'ExDate']] = div[['Annc. Date', 'Record Date', 'ExDate']].apply(pd.to_datetime, errors = 'coerce', format = "%d-%m-%Y")

div.to_csv("C:\\Users\\krath002\\Desktop\\Ajna.ai\\DivData.csv")

