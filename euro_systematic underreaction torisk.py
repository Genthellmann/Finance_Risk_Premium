#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 25 22:08:51 2021

@author: johannesthellmann
"""



import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import datetime 
import warnings
import statsmodels.api as sm



data_path = '/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/data/csv/return_eurostoxx.csv'
cols_to_use = ['DATES','ES','PX_BID','PX_ASK','PX_LAST','MATURITY','DAYS_TO_MATURITY',
               'FORECAST','PREMIUM','PX_LAST_EOM','MATURITY_EOM','MATURITY_MONTH','XR','VIX_R']
dtype_dic= {'DATES':str,'ES':float,'PX_BID':float,'PX_ASK':float,'PX_LAST':float,'MATURITY':str,'DAYS_TO_MATURITY':int,
               'FORECAST':float,'PREMIUM':float,'PX_LAST_EOM':float,'MATURITY_EOM':str,'MATURITY_MONTH':str,'XR':float,'VIX_R':float}
vix_p = pd.read_csv(data_path, sep=',', decimal='.', usecols=cols_to_use, dtype=dtype_dic)

#Index erstellen zuerst als extra Spalte dann als index und behalten für differenz zu maturity date
vix_p['INDEX'] = vix_p['DATES']
vix_p = vix_p.set_index(vix_p['INDEX'])
vix_p = vix_p.drop(['INDEX'], axis=1)

#make date time object
vix_p['DATES'] = pd.to_datetime(vix_p['DATES']) #Spalte ins Format to_datetime bringen
vix_p['MATURITY'] = pd.to_datetime(vix_p['MATURITY'])



#=======================================
#Regression with VIX

#Nur einen Zeitraum des Datensatzes verwenden, sonst start date von oben verwenden 
#für VIX

#voller ZeITRAUM Daten von 01.01.2005 bis 30.10.2020
startdate = pd.to_datetime('2018-10-01')
enddate = pd.to_datetime('2020-05-21')

# #ex 2020
# startdate = pd.to_datetime('2005-01-01')
# enddate = pd.to_datetime('2020-01-01')

# #2019 und 2020
# startdate = pd.to_datetime('2019-01-01')
# enddate = pd.to_datetime('2020-05-21')

dates_to_use = (vix_p['DATES'] >= pd.to_datetime(startdate)) & (vix_p['DATES'] < pd.to_datetime(enddate))
vix_p = vix_p.loc[dates_to_use]

#VIX
VIX = vix_p['ES'].to_numpy()
VIX_0 = VIX[3:] 
VIX_1 = VIX[2:-1]
VIX_2 = VIX[1:-2]
VIX_3 = VIX[:-3]

#X
#vix_return
vix_r = vix_p['VIX_R'].to_numpy()
vix_r_0 = vix_r[3:] *100
vix_r_1 = vix_r[2:-1] *100
vix_r_2 = vix_r[1:-2] *100
vix_r_3 = vix_r[:-3] *100

#Design Matrix
X_return = pd.DataFrame({'Risk_t': VIX_0,'Risk_1': VIX_1,'Risk_2': VIX_2,'Risk_3': VIX_3,
                          'VIXR_1': vix_r_1, 'VIXR_2': vix_r_2,'VIXR_3': vix_r_3 })

X = sm.add_constant(X_return)
Y = vix_r_0

model = sm.OLS(Y, X)
results = model.fit(cov_type = 'HAC', cov_kwds = {'maxlags':1})
print(results.summary())