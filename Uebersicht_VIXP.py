#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 21:10:39 2021

@author: johannesthellmann
"""


import numpy as np
import pandas as pd


data_path =  '/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/data/csv/arma_2.csv'
#Anmerkung: Die hier verwendete ARMA.csv unterscheidet sich von der in vix_arma.py erzeugten arma.csv insofern, dass fehlerhafte Future-Werte (falsche Stelle des Dezimalpunktes)
#und das Premium für diese Werte
cols_to_use = ['DATES','VIX','PX_BID','PX_ASK','PX_LAST','MATURITY','DAYS_TO_MATURITY','FORECAST','PREMIUM']
dtype_dic= {'DATES':str,'VIX':float,'PX_BID':float,'PX_ASK':float,'PX_LAST':float,'MATURITY':str,
            'DAYS_TO_MATURITY':float,'FORECAST':float, 'PREMIUM':float}
vix_p = pd.read_csv(data_path, sep=',', decimal='.', usecols=cols_to_use, dtype=dtype_dic)

vix_p['DATES'] = pd.to_datetime(vix_p['DATES'])
#Nur einen Zeitraum des Datensatzes verwenden, sonst start date von oben verwenden 
startdate = pd.to_datetime('2020-02-01')
enddate = pd.to_datetime('2020-05-21')


dates_to_use = (vix_p['DATES'] >= pd.to_datetime(startdate)) & (vix_p['DATES'] < pd.to_datetime(enddate))
vix_p = vix_p.loc[dates_to_use]

#summary statistics
vix_p['PREMIUM'].describe()

#calculate rest of the quantiles
vix_parray = vix_p['PREMIUM'].to_numpy()
np.quantile(vix_parray, [0.01, 0.05, 0.95, 0.99])

#calculate number of days with premium < 0
za = (vix_parray<0).sum()
percentage = za/len(vix_parray)


#======================================
#Übersicht EuroStoxx
#======================================


data_path =  '/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/data/csv/eurostoxx_arma.csv'
cols_to_use = ['DATES','ES','PX_BID','PX_ASK','PX_LAST','MATURITY','DAYS_TO_MATURITY','FORECAST','PREMIUM']
dtype_dic= {'DATES':str,'ES':float,'PX_BID':float,'PX_ASK':float,'PX_LAST':float,'MATURITY':str,'DAYS_TO_MATURITY':float,'FORECAST':float,'PREMIUM':float}
es = pd.read_csv(data_path, sep=',', decimal='.', usecols=cols_to_use, dtype=dtype_dic)
es['index'] = es['DATES']
es = es.set_index(es['index'])
es = es.drop(['index'], axis=1)
es['DATES'] = pd.to_datetime(es['DATES']) #Spalte ins Format to_datetime bringen
es['MATURITY'] = pd.to_datetime(es['MATURITY'])



#eurostoxx voller Zeitraum 01.12.2009 bis 07.05.2021
startdate = pd.to_datetime('2020-01-25')
enddate = pd.to_datetime('2020-05-21')
dates_to_use = (es['DATES'] >= pd.to_datetime(startdate)) & (es['DATES'] <= pd.to_datetime(enddate))
es = es.loc[dates_to_use]

#summary statistics
es['PREMIUM'].describe()

#calculate rest of the quantiles
es_array = es['PREMIUM'].to_numpy()
quantile = np.quantile(es_array, [0.01, 0.05, 0.95, 0.99])

#calculate number of days with premium < 0
za = (es_array<0).sum()
percentage = za/len(es_array)

