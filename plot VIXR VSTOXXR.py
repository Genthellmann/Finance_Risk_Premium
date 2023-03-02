#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 27 18:01:53 2021

@author: johannesthellmann
"""


 
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import datetime 
import warnings

data_path1 = '/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/data/csv/vix_r.csv'
data_path2 = '/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/data/csv/return_eurostoxx.csv'

#VIXR
cols_to_use = ['DATES','VIX_R']
dtype_dic= {'DATES':str, 'VIX_R':float}
vix_r = pd.read_csv(data_path1, sep=',', decimal='.', usecols=cols_to_use, dtype=dtype_dic)

#Index erstellen zuerst als extra Spalte dann als index und behalten für differenz zu maturity date
vix_r['INDEX'] = vix_r['DATES']
vix_r = vix_r.set_index(vix_r['INDEX'])
vix_r = vix_r.drop(['INDEX'], axis=1)

#make date time object
vix_r['DATES_VIX'] = pd.to_datetime(vix_r['DATES']) #Spalte ins Format to_datetime bringen
vix_r = vix_r.drop(['DATES'], axis=1)



#VSTOXXR
cols_to_use = ['DATES','VIX_R']
dtype_dic= {'DATES':str,'VIX_R':float}
vstoxx_r = pd.read_csv(data_path2, sep=',', decimal='.', usecols=cols_to_use, dtype=dtype_dic)

#Index erstellen zuerst als extra Spalte dann als index und behalten für differenz zu maturity date
vstoxx_r['INDEX'] = vstoxx_r['DATES']
vstoxx_r = vstoxx_r.set_index(vstoxx_r['INDEX'])
vstoxx_r = vstoxx_r.drop(['INDEX'], axis=1)

#make date time object
vstoxx_r['DATES_VSTOXX'] = pd.to_datetime(vstoxx_r['DATES']) #Spalte ins Format to_datetime bringen
vstoxx_r = vstoxx_r.drop(['DATES'], axis=1)
vstoxx_r['VSTOXX_R'] = vstoxx_r['VIX_R']
vstoxx_r = vstoxx_r.drop(['VIX_R'], axis=1)



concat = pd.concat([vix_r, vstoxx_r], axis = 1)


#Nur einen Zeitraum des Datensatzes verwenden, sonst start date von oben verwenden 
startdate = pd.to_datetime('2006-01-01')
enddate = pd.to_datetime('2020-05-21')
dates_to_use = (concat['DATES_VIX'] >= pd.to_datetime(startdate)) & (concat['DATES_VIX'] < pd.to_datetime(enddate))
concat = concat.loc[dates_to_use]


#====================
#Plot
#====================

#only use the rows with entrys for xr and vixr
mask_xr_values = concat['VIX_R'] > -1000
concat_plot = concat.loc[mask_xr_values]
concat_plot = concat_plot.dropna()

#plot
fig = plt.figure(figsize=[7.5, 3]); # Set dimensions for figure
ax = fig.add_subplot()
y = concat_plot['VIX_R']
x = concat_plot['DATES_VIX']

y1 = concat_plot['VSTOXX_R']
x1 = concat_plot['DATES_VSTOXX']

ax.plot(x,y, label = 'VIXR')
ax.plot(x1,y1, label = 'VSTOXXR')

ax.axhline(y=0, color='k') #show 0 level
ticks = pd.to_datetime(['2010-01','2012-01','2014-01','2016-01','2018-01','2020-01'])
ax.set_xticks(ticks)
ax.set_xticklabels(['Jan 10','Jan 12','Jan 14','Jan 16','Jan 18','Jan 20'])
plt.legend(loc = 2)
plt.savefig('/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/Präsentation/VIXR_VSTOXXR through time.pdf', bbox_inches = 'tight')

