#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  4 09:37:30 2021

@author: johannesthellmann
"""


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import datetime 
import warnings
import statsmodels.api as sm


data_path =  '/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/data/csv/arma_2.csv'
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

#VVIX Data
data_path1 = '/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/data/csv/VVIX.csv'
cols_to_use1 = ['Dates', 'PX_LAST']
dtype_dic1 = {'Dates':str, 'PX_LAST':float}
vvix = pd.read_csv(data_path1, sep=',', decimal='.', usecols=cols_to_use1)
vvix['INDEX'] = vvix['Dates']
vvix = vvix.set_index(vvix['INDEX'])
vvix = vvix.drop(['INDEX'], axis=1)
vvix['Dates_VVIX'] = pd.to_datetime(vvix['Dates']) #Spalte ins Format to_datetime bringen
vvix['PX_LAST_VVIX'] = vvix['PX_LAST']
vvix = vvix.drop(['PX_LAST'], axis=1)



#concatenate vix_p and vix_eom
vix_p = pd.concat([vix_p, vvix], axis=1)




#Nur einen Zeitraum des Datensatzes verwenden, sonst start date von oben verwenden 
startdate = pd.to_datetime('2006-03-03')
enddate = pd.to_datetime('2020-01-01')
dates_to_use = (vix_p['DATES'] >= pd.to_datetime(startdate)) & (vix_p['DATES'] < pd.to_datetime(enddate))
vix_p = vix_p.loc[dates_to_use]



mask_isna = vix_p['PX_LAST_VVIX'].isna()
vix_p = vix_p.dropna(subset=['PX_LAST_VVIX'])




#Daily return
last_prize_t = vix_p['PX_LAST'].to_numpy() 
vix_hat = vix_p['FORECAST'].to_numpy()
days_to_mat = vix_p['DAYS_TO_MATURITY'].to_numpy()

vix_r = (vix_hat/last_prize_t)**(1/days_to_mat) -1

#VIX Index
VIX = vix_p['VIX'].to_numpy()
VIX_0 = VIX[3:]
VIX_1 = VIX[2:-1]
VIX_2 = VIX[1:-2]
VIX_3 = VIX[:-3]

#X
#vix_return
vix_r_1 = vix_r[2:-1]
vix_r_2 = vix_r[1:-2]
vix_r_3 = vix_r[:-3]

#Y
vix_r_0 = vix_r[3:]

#Design Matrix
X_return = pd.DataFrame({'Risk_t': VIX_0,'Risk_1': VIX_1,'Risk_2': VIX_2,'Risk_3': VIX_3,
                          'VIXR_1': vix_r_1, 'VIXR_2': vix_r_2,'VIXR_3': vix_r_3 })

X = sm.add_constant(X_return)
Y = vix_r_0

model = sm.OLS(Y, X)
results = model.fit()
print(results.summary())

#Regression with VVIX
#Daily return
last_prize_t = vix_p['PX_LAST'].to_numpy() 
vix_hat = vix_p['FORECAST'].to_numpy()
days_to_mat = vix_p['DAYS_TO_MATURITY'].to_numpy()

vix_r = (vix_hat/last_prize_t)**(1/days_to_mat) -1

#VIX Index
VVIX = vix_p['PX_LAST_VVIX'].to_numpy()
VVIX_0 = VVIX[3:]
VVIX_1 = VVIX[2:-1]
VVIX_2 = VVIX[1:-2]
VVIX_3 = VVIX[:-3]

#X
#vix_return
vix_r_1 = vix_r[2:-1]
vix_r_2 = vix_r[1:-2]
vix_r_3 = vix_r[:-3]

#Y
vix_r_0 = vix_r[3:]

#Design Matrix
X_return = pd.DataFrame({'Risk_t': VVIX_0,'Risk_1': VVIX_1,'Risk_2': VVIX_2,'Risk_3': VVIX_3,
                         'VIXR_1': vix_r_1, 'VIXR_2': vix_r_2,'VIXR_3': vix_r_3 })

X = sm.add_constant(X_return)
Y = vix_r_0

model = sm.OLS(Y, X)
results = model.fit(cov_type = 'HAC', cov_kwds = {'maxlags':3})
print(results.summary())




