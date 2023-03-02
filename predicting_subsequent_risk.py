#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 15:50:02 2021

@author: johannesthellmann
"""


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import datetime 
import warnings

data_path =  '/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/data/csv/arma_2.csv'
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

#==========================
#Data with correct EOM values
#==========================

data_path1 =  '/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/data/csv/vix_f_EOM_2.csv'
cols_to_use = ['Dates', 'CURRENT_CONTRACT_MONTH_YR', 'LAST_PRICE', 'PX_BID', 'PX_ASK', 'PX_LAST', 'Maturity']
dtype_dic= {'Dates':str,'CURRENT_CONTRACT_MONTH_YR':float,'LAST_PRICE':float, 'PX_BID':float,'PX_ASK':float,'PX_LAST':float,'Maturity':str}
vix_eom = pd.read_csv(data_path1, sep=',', decimal='.', usecols=cols_to_use, dtype=dtype_dic)
vix_eom['INDEX'] = vix_eom['Dates']
vix_eom = vix_eom.set_index(vix_eom['INDEX'])
vix_eom = vix_eom.drop(['INDEX'], axis=1)
vix_eom['PX_LAST_EOM'] = vix_eom['PX_LAST']
vix_eom['MATURITY_EOM'] = vix_eom['Maturity']
vix_eom['MATURITY_EOM'] = pd.to_datetime(vix_eom['MATURITY_EOM'])
vix_eom = vix_eom.drop(['CURRENT_CONTRACT_MONTH_YR', 'LAST_PRICE', 'PX_BID', 'PX_ASK', 'PX_LAST', 'Dates', 'Maturity'], axis = 1)

#==========================
#SP500 Data
#==========================

data_path_sp500 = '/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/data/csv/SP500.csv'
cols_to_use = ['Dates','PX_LAST']
dtype_dic= {'Dates':str,'PX_LAST':float}
sp500 = pd.read_csv(data_path_sp500, usecols=cols_to_use, dtype=dtype_dic)
sp500['INDEX'] = sp500['Dates']
sp500 = sp500.set_index(sp500['INDEX'])
sp500['PX_LAST_SP500'] = sp500['PX_LAST']
sp500 = sp500.drop(['INDEX'], axis=1)
sp500 = sp500.drop(['Dates'], axis=1)
sp500 = sp500.drop(['PX_LAST'], axis=1)

#==========================
#Monthly VIX Return Data
#==========================
data_path_vixr =  '/Users/johannesthellmann/Desktop/return.csv' #Anmerkung return.csv: Der Return für Month t trägt das Datum des letzten Tages von Monat t-1 -> wichtig für Nachfolgende Regression
cols_to_use = ['DATES','VIX_R']
dtype_dic= {'DATES':str,'VIX_R':float}
vix_r = pd.read_csv(data_path_vixr, sep=',', decimal='.', usecols=cols_to_use, dtype=dtype_dic)
vix_r['INDEX'] = vix_r['DATES']
vix_r = vix_r.set_index(vix_r['INDEX'])
vix_r['DATES_VIXR'] = pd.to_datetime(vix_r['DATES']) #Spalte ins Format to_datetime bringen
vix_r = vix_r.drop(['INDEX'], axis=1)
vix_r = vix_r.drop(['DATES'], axis=1)



#concatenate vix_p and vix_eom
vix_p = pd.concat([vix_p, vix_eom, sp500, vix_r], axis=1)

#First future prizes from 2005-01-01, last from 2020-10-30
#cheng uses until end of may 2020

#Nur einen Zeitraum des Datensatzes verwenden, sonst start date von oben verwenden Arma hat Daten von 03.01.2005 - 24.11.2020
#Hier drauf achten, den letzten Tag des vorherigen Monats mitzunehmen
startdate = pd.to_datetime('2005-01-01')
enddate = pd.to_datetime('2020-11-25')
dates_to_use = (vix_p['DATES'] >= pd.to_datetime(startdate)) & (vix_p['DATES'] < pd.to_datetime(enddate))
vix_p = vix_p.loc[dates_to_use]

#=================================
#Berechnen der Daily-return for fully collaterized 1-month Vix-Futures
#=================================

#Daily return
dates_daily = vix_p['DATES'].tolist()
vix_hat = vix_p['FORECAST'].array

last_prize_t = vix_p['PX_LAST_EOM'].array 
days_to_mat = vix_p['DAYS_TO_MATURITY']
vixr_daily = (vix_hat/last_prize_t)**(1/days_to_mat) -1 #Cheng uses VIXR-2 to estimate xr
df_daily = pd.DataFrame({'DATES': dates_daily, 'VIXR_DAILY' : vixr_daily})
vix_p['VIXR_DAILY'] = df_daily['VIXR_DAILY']

#=================================
#Berechnen der Daily-log-return for SP500
#=================================

SP500_daily = np.log(vix_p['PX_LAST_SP500'].to_numpy()[1:]) - np.log(vix_p['PX_LAST_SP500'].to_numpy()[:-1])
begin_zero = [0]
SP500_daily = np.concatenate((begin_zero,SP500_daily), axis = 0)

vix_p['LOGR_SP500_DAILY'] = SP500_daily


#Verwende nur den Monat des datetime objects
vix_p['MATURITY_MONTH'] = vix_p['MATURITY'].dt.to_period('M')
vix_p['MATURITY_EOM'] = vix_p['MATURITY_EOM'].dt.to_period('M')

years = ['2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020']
#years = ['2005']

months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
#months = ['01', '02', '03']

#Berechnung der monthly SD
for y in years:
    for m in months:
        
        try:
            #only use dates of current maturity month t+1
            cur_month = y + '-' + m
            
            mask_month = (vix_p['MATURITY_EOM'] == pd.to_datetime(cur_month).to_period('M'))
            vixp_curmonth = vix_p.loc[mask_month]
            #print(cur_month)
            #print(vixp_curmonth)
            
            #sd of Daily Vix Return
            first_day = vixp_curmonth.index.min()
            vix_p.loc[first_day,['SD_VIXR']] = vixp_curmonth['VIXR_DAILY'].std()
            #print(vix_p.loc[first_day,['SD_VIXR']])
            
            #sd of SP500
            vix_p.loc[first_day,['SD_SP500']] = vixp_curmonth['LOGR_SP500_DAILY'].std()
            #print(vix_p.loc[first_day,['SD_SP500']])
        
        except:
            print('Not a valid maturity date: ' + cur_month)
        


#=================================
#VIXR
#=================================
import statsmodels.api as sm
#standard deviation
sd = vix_p.dropna(subset=['SD_VIXR'])
sd = sd['SD_VIXR'].to_numpy()
sd_0 = sd[3:]
sd_1 = sd[2:-1]
sd_2 = sd[1:-2]
sd_3 = sd[:-3]

#VIXR
VIXR = vix_p.dropna(subset=['VIX_R'])
VIXR = VIXR['VIX_R'].to_numpy()
VIXR_1 = VIXR[2:-1]
VIXR_2 = VIXR[1:-2]
VIXR_3 = VIXR[:-3]

#Design Matrix
X_design = pd.DataFrame({'VIXR_1': VIXR_1, 'VIXR_2': VIXR_2,'VIXR_3': VIXR_3, 'sd_1': sd_1, 'sd2': sd_2, 'sd3': sd_3 })

X = sm.add_constant(X_design)
Y = sd_0

model = sm.OLS(Y, X)
results = model.fit()
print(results.summary())


#=================================
#SP500
#=================================
import statsmodels.api as sm
#standard deviation
sd = vix_p.dropna(subset=['SD_SP500'])
sd = sd['SD_SP500'].to_numpy()
sd_0 = sd[3:]
sd_1 = sd[2:-1]
sd_2 = sd[1:-2]
sd_3 = sd[:-3]

#VIXR
VIXR = vix_p.dropna(subset=['VIX_R'])
VIXR = VIXR['VIX_R'].to_numpy()
VIXR_1 = VIXR[2:-1]
VIXR_2 = VIXR[1:-2]
VIXR_3 = VIXR[:-3]

#Design Matrix
X_design = pd.DataFrame({'VIXR_1': VIXR_1, 'VIXR_2': VIXR_2,'VIXR_3': VIXR_3, 'sd_1': sd_1, 'sd2': sd_2, 'sd3': sd_3 })

X = sm.add_constant(X_design)
Y = sd_0

model = sm.OLS(Y, X)
results = model.fit()
print(results.summary())

