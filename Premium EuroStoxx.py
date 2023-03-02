#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 08:35:23 2021

@author: johannesthellmann
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime 
import holidays

data_path =  '/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/data/csv/eurostoxx_arma.csv'
cols_to_use = ['DATES','ES','PX_BID','PX_ASK','PX_LAST','MATURITY','DAYS_TO_MATURITY','FORECAST','PREMIUM']
dtype_dic= {'DATES':str,'ES':float,'PX_BID':float,'PX_ASK':float,'PX_LAST':float,'MATURITY':str,'DAYS_TO_MATURITY':float,'FORECAST':float,'PREMIUM':float}
es = pd.read_csv(data_path, sep=',', decimal='.', usecols=cols_to_use, dtype=dtype_dic)

#Index erstellen zuerst als extra Spalte dann als index und behalten für differenz zu maturity date
es['index'] = es['DATES']
es = es.set_index(es['index'])
es = es.drop(['index'], axis=1)

#make date time object
es['DATES'] = pd.to_datetime(es['DATES']) #Spalte ins Format to_datetime bringen
es['MATURITY'] = pd.to_datetime(es['MATURITY'])

#====================
#Plot
#====================
startdate = pd.to_datetime('2020-02-01')
enddate = pd.to_datetime('2020-06-01')

#y-Werte
mask_plot = (es['DATES'] > pd.to_datetime(startdate)) & (es['DATES'] <= pd.to_datetime(enddate))
es_plot = es.loc[mask_plot]

#plot
fig = plt.figure(figsize=[8, 6]); # Set dimensions for figure
ax = fig.add_subplot()
x = es_plot['DATES']
y = es_plot['PREMIUM']
ax.plot(x,y)
ax.axhline(y=0, color='k') #show 0 level
ticks = pd.to_datetime(['2020-02-01', '2020-03-01','2020-04-01','2020-05-01', '2020-06-01'])
ax.set_xticks(ticks)
ax.set_xticklabels(['Feb 01', 'Mar 01','Apr 01', 'May 01', 'Jun 01'])


# path = '/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/data/csv/S&P500.csv'
# cols_to_use = ['Dates','PX_LAST']
# dtype_dic= {'Dates':str,'PX_ASK':float}
# sp500 = pd.read_csv(path, delimiter=';', decimal=',', usecols=cols_to_use, dtype=dtype_dic)
# sp500['Dates'] = pd.to_datetime(sp500['Dates'], format = '%d.%m.%y')
# sp500.to_csv('/Users/johannesthellmann/Desktop/SP500.csv', index = False)

mask = es_plot['PREMIUM'] < -8
es_plot = es_plot.loc[mask]
