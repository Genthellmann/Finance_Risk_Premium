#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 11:09:31 2021

@author: johannesthellmann
"""
 
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import datetime 
import warnings

data_path =  '/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/data/csv/ARMA.csv'
#Anmerkung: Die hier verwendete ARMA.csv unterscheidet sich von der in vix_arma.py erzeugten arma.csv insofern, dass fehlerhafte Future-Werte (falsche Stelle des Dezimalpunktes)
#und das Premium für diese Werte
cols_to_use = ['DATES','VIX','PX_BID','PX_ASK','PX_LAST','MATURITY','DAYS_TO_MATURITY','FORECAST','PREMIUM']
dtype_dic= {'DATES':str,'VIX':float,'PX_BID':float,'PX_ASK':float,'PX_LAST':float,'MATURITY':str,
            'DAYS_TO_MATURITY':float,'FORECAST':float, 'PREMIUM':float}
vix_p = pd.read_csv(data_path, sep=',', decimal='.', usecols=cols_to_use, dtype=dtype_dic)

#Index erstellen zuerst als extra Spalte dann als index und behalten für differenz zu maturity date
vix_p['INDEX'] = vix_p['DATES']
vix_p = vix_p.set_index(vix_p['INDEX'])
vix_p = vix_p.drop(['INDEX'], axis=1)

#make date time object
vix_p['DATES'] = pd.to_datetime(vix_p['DATES']) #Spalte ins Format to_datetime bringen
vix_p['MATURITY'] = pd.to_datetime(vix_p['MATURITY'])

#Premium neu berechnen, aufgrund angepasster .csv file
vix_p['PREMIUM2'] = vix_p['PX_LAST'] - vix_p['FORECAST']

vix_p['PREMIUM2'] = vix_p['PX_LAST'] - vix_p['FORECAST']


# #==========================
# #Data with correct EOM values
# #==========================

# data_path1 =  '/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/data/csv/vix_f_EOM_2.csv'
# #Anmerkung: Die hier verwendete ARMA.csv unterscheidet sich von der in vix_arma.py erzeugten arma.csv insofern, dass fehlerhafte Future-Werte (falsche Stelle des Dezimalpunktes)
# #und das Premium für diese Werte
# cols_to_use = ['Dates', 'CURRENT_CONTRACT_MONTH_YR', 'LAST_PRICE', 'PX_BID', 'PX_ASK', 'PX_LAST', 'Maturity']
# dtype_dic= {'Dates':str,'CURRENT_CONTRACT_MONTH_YR':float,'LAST_PRICE':float, 'PX_BID':float,'PX_ASK':float,'PX_LAST':float,'Maturity':str}
# vix_eom = pd.read_csv(data_path1, sep=',', decimal='.', usecols=cols_to_use, dtype=dtype_dic)

# #Index erstellen zuerst als extra Spalte dann als index und behalten für differenz zu maturity date
# vix_eom['INDEX'] = vix_eom['Dates']
# vix_eom = vix_eom.set_index(vix_eom['INDEX'])
# vix_eom = vix_eom.drop(['INDEX'], axis=1)

# #Rename col to distinguish
# vix_eom['PX_LAST_EOM'] = vix_eom['PX_LAST']

# vix_eom['MATURITY_EOM'] = vix_eom['Maturity']
# vix_eom['MATURITY_EOM'] = pd.to_datetime(vix_eom['MATURITY_EOM'])

# vix_eom = vix_eom.drop(['CURRENT_CONTRACT_MONTH_YR', 'LAST_PRICE', 'PX_BID', 'PX_ASK', 'PX_LAST', 'Dates', 'Maturity'], axis = 1)

# #concatenate vix_p and vix_eom
# vix_p = pd.concat([vix_p, vix_eom], axis=1)


#First future prizes from 2005-01-01, last from 2020-10-30
#cheng uses until end of may 2020

#Nur einen Zeitraum des Datensatzes verwenden, sonst start date von oben verwenden 
startdate = pd.to_datetime('2005-01-01')
enddate = pd.to_datetime('2005-01-10')
dates_to_use = (vix_p['DATES'] >= pd.to_datetime(startdate)) & (vix_p['DATES'] < pd.to_datetime(enddate))
vix_p = vix_p.loc[dates_to_use]

# #check for na
# mask1 = vix_p['DATES'].isna()
# check1 = vix_p.loc[mask1]

# mask2 = vix_p['PX_LAST'].isna()
# check2 = vix_p.loc[mask2]

#Daily return
last_prize = vix_p['PX_LAST'].array
xr = last_prize[1:]/last_prize[:-1] -1


#Nur einen Zeitraum des Datensatzes verwenden, sonst start date von oben verwenden 
startdate = pd.to_datetime('2006-01-01')
enddate = pd.to_datetime('2019-12-31')
dates_to_use = (vix_p['DATES'] >= pd.to_datetime(startdate)) & (vix_p['DATES'] < pd.to_datetime(enddate))
vix_p = vix_p.loc[dates_to_use]

#====================
#Plot
#====================

#only use the rows with entrys for xr and vixr
mask_xr_values = vix_p['XR'] > -1000
vix_plot = vix_p.loc[mask_xr_values]

#plot
fig = plt.figure(figsize=[15, 7.5]); # Set dimensions for figure
ax = fig.add_subplot()
y = vix_plot['VIX_R']
x = vix_plot['DATES']
ax.plot(x,y)
ax.axhline(y=0, color='k') #show 0 level
ticks = pd.to_datetime(['2006-01','2008-01','2010-01','2012-01','2014-01','2016-01','2018-01','2020-01'])
ax.set_xticks(ticks)
ax.set_xticklabels(['Jan 06','Jan 08','Jan 10','Jan 12','Jan 14','Jan 16','Jan 18','Jan 20'])


#=================
#Linear Regression of tomorrows futures prize changes on tomorrows premium
#=================

import statsmodels.api as sm


X = sm.add_constant(vix_plot['VIX_R'])
Y = vix_plot['XR']

model = sm.OLS(Y, X)
results = model.fit()
print(results.summary())


