# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 02:35:39 2017

@author: krath002
"""

import pandas as pd
import pandas_datareader.data as web
import datetime
import os
from copy import deepcopy
from pandas_datareader._utils import RemoteDataError

os.chdir("C:\\Users\\krath002\\Desktop\\Ajna.ai\\")

mapping = pd.read_csv("Mapping.csv")

data_columns = ['Date','Symbol','Series','Open','High','Low','Close','Volume']

start_date = datetime.datetime(2000, 1, 1)
end_date = datetime.datetime(2017, 9, 21)

weekday = [x for x in pd.date_range(start_date, end_date) if x.weekday() < 5]

for i in range(0,len(mapping)):
    ticker = mapping.iloc[i]["Symbol"]
    if i != 6:
        fetch_data = False
        while not fetch_data:
            try:
                fetch_data = True
                tmp = web.DataReader(ticker+".NS", "yahoo", start_date, end_date)
            except RemoteDataError:
                fetch_data = False
                pass
            
    tmp1 = deepcopy(tmp)
    tmp1.fillna(method = "ffill", inplace = True)
    tmp1.drop([d for d in tmp1.index if d not in weekday], axis = 0, inplace = True)
    tmp1.drop("Adj Close", axis = 1, inplace = True)
    
    dates = [x for x in weekday if x >= tmp.index[0]]
    price_data = pd.DataFrame(index = dates, columns = data_columns)
    price_data.loc[tmp1.index, tmp1.columns] = tmp1
    
    for col in list(mapping.columns):
        if col not in tmp1.columns and col != "Company Name":
            price_data[col] = mapping.iloc[i][col]
    
    price_data.fillna(method = "ffill", inplace = True)    
    price_data["Date"] = [dt.strftime("%Y/%m/%d") for dt in price_data.index]
    
    price_data.to_csv("Data\\"+ticker+".csv", index = False)
    
    