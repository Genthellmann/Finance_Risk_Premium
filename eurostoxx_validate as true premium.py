#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 23:04:52 2021

@author: johannesthellmann
"""

 
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import datetime 
import warnings

data_path =  '/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/data/csv/eurostoxx_arma.csv'
#Anmerkung: Die hier verwendete ARMA.csv unterscheidet sich von der in vix_arma.py erzeugten arma.csv insofern, dass fehlerhafte Future-Werte (falsche Stelle des Dezimalpunktes)
#und das Premium für diese Werte
cols_to_use = ['DATES','ES','PX_BID','PX_ASK','PX_LAST','MATURITY','DAYS_TO_MATURITY','FORECAST','PREMIUM']
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

data_path1 =  '/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/data/csv/eurostoxx_eom.csv'
#Anmerkung: Die hier verwendete ARMA.csv unterscheidet sich von der in vix_arma.py erzeugten arma.csv insofern, dass fehlerhafte Future-Werte (falsche Stelle des Dezimalpunktes)
#und das Premium für diese Werte
cols_to_use = ['Dates', 'CURRENT_CONTRACT_MONTH_YR', 'LAST_PRICE', 'PX_BID', 'PX_ASK', 'PX_LAST', 'Maturity']
dtype_dic= {'Dates':str,'CURRENT_CONTRACT_MONTH_YR':float,'LAST_PRICE':float, 'PX_BID':float,'PX_ASK':float,'PX_LAST':float,'Maturity':str}
vix_eom = pd.read_csv(data_path1, sep=',', decimal='.', usecols=cols_to_use, dtype=dtype_dic)

#Index erstellen zuerst als extra Spalte dann als index und behalten für differenz zu maturity date
vix_eom['INDEX'] = vix_eom['Dates']
vix_eom = vix_eom.set_index(vix_eom['INDEX'])
vix_eom = vix_eom.drop(['INDEX'], axis=1)

#Rename col to distinguish
vix_eom['PX_LAST_EOM'] = vix_eom['PX_LAST']

vix_eom['MATURITY_EOM'] = vix_eom['Maturity']
vix_eom['MATURITY_EOM'] = pd.to_datetime(vix_eom['MATURITY_EOM'])


vix_eom = vix_eom.drop(['CURRENT_CONTRACT_MONTH_YR', 'LAST_PRICE', 'PX_BID', 'PX_ASK', 'PX_LAST', 'Dates', 'Maturity'], axis = 1)


#concatenate vix_p and vix_eom
vix_p = pd.concat([vix_p, vix_eom], axis=1)

#First future prizes from 200-12-01, last from 2020-10-30
#cheng uses until end of may 2020

#Nur einen Zeitraum des Datensatzes verwenden, sonst start date von oben verwenden 
startdate = pd.to_datetime('2009-12-01')
enddate = pd.to_datetime('2020-01-01')
dates_to_use = (vix_p['DATES'] >= pd.to_datetime(startdate)) & (vix_p['DATES'] < pd.to_datetime(enddate))
vix_p = vix_p.loc[dates_to_use]

# #check for na
# mask1 = vix_p['DATES'].isna()
# check1 = vix_p.loc[mask1]

# mask2 = vix_p['PX_LAST'].isna()
# check2 = vix_p.loc[mask2]

#Verwende nur den Monat des datetime objects
vix_p['MATURITY_MONTH'] = vix_p['MATURITY'].dt.to_period('M')
vix_p['MATURITY_EOM'] = vix_p['MATURITY_EOM'].dt.to_period('M')


years = ['2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020']
#years = ['2005']

months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
#months = ['01', '02', '03']

#create to columns for results
vix_p['XR'] = -1000
vix_p['VIX_R'] = -1000


#Die Berechnung läuft nach der Maturity, xr wird aber für Februar ausgerechnet

for y in years:
    for m in months:
        
        try:
            #only use dates of current maturity month t+1
            cur_month = y + '-' + m
            
            
            mask_month = (vix_p['MATURITY_MONTH'] == pd.to_datetime(cur_month).to_period('M'))
            vixp_curmonth = vix_p.loc[mask_month]
            #print(cur_month)
            #print(vixp_curmonth)
            
            #With correct EOM Price
            mask_month_eom = (vix_p['MATURITY_EOM'] == pd.to_datetime(cur_month).to_period('M'))
            vixp_eom = vix_p.loc[mask_month_eom]
            
            #last day of current month
            #get index
            last_day = vixp_eom.index.max()
            last_day_data = vixp_eom.loc[last_day]
            
            #print('lastday'+ str(last_day))
            
            #Last day of previous month: is the first day of the maturity as for the premium
            first_day = vixp_curmonth.index.min()
            first_day_data = vixp_curmonth.loc[first_day]
            F_t1 = first_day_data['PX_LAST']
            #print('firstday' + str(F_t1))
            
            #monthly excess return from fully collateralized long position
            vix_p.loc[first_day,['XR']] = last_day_data['PX_LAST_EOM']/F_t1 - 1
    
            #monthly expected excess return
            vix_p.loc[first_day, ['VIX_R']] = (first_day_data['FORECAST']/F_t1)**(21/first_day_data['DAYS_TO_MATURITY']) - 1
        
        except:
            print('Not a valid maturity date: ' + cur_month)
        



#Nur einen Zeitraum des Datensatzes verwenden, sonst start date von oben verwenden 
startdate = pd.to_datetime('2020-01-01')
enddate = pd.to_datetime('2020-05-21')
dates_to_use = (vix_p['DATES'] >= pd.to_datetime(startdate)) & (vix_p['DATES'] < pd.to_datetime(enddate))
vix_p = vix_p.loc[dates_to_use]

#vix_p.to_csv('/Users/johannesthellmann/Desktop/vix_r.csv', index = False)

#====================
#Plot
#====================

#only use the rows with entrys for xr and vixr
mask_xr_values = vix_p['XR'] > -1000
vix_plot = vix_p.loc[mask_xr_values]

#plot
fig = plt.figure(figsize=[25, 10]); # Set dimensions for figure
ax = fig.add_subplot()
y = vix_plot['VIX_R']
x = vix_plot['DATES']
ax.plot(x,y, label = 'VSTOXXR')
ax.axhline(y=0, color='k') #show 0 level
ticks = pd.to_datetime(['2006-01','2008-01','2010-01','2012-01','2014-01','2016-01','2018-01','2020-01'])
ax.set_xticks(ticks)
ax.set_xticklabels(['Jan 06','Jan 08','Jan 10','Jan 12','Jan 14','Jan 16','Jan 18','Jan 20'])
plt.legend(loc = 2)
#plt.savefig('/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/results/VSTOXXR through time.png', bbox_inches = 'tight')

#vix_plot.to_csv('/Users/johannesthellmann/Desktop/return_eurostoxx.csv', index=False)

#=================
#Linear Regression of tomorrows futures prize changes on tomorrows premium
#=================

import statsmodels.api as sm


X = sm.add_constant(vix_plot['VIX_R'])
Y = vix_plot['XR']

model = sm.OLS(Y, X)
results = model.fit(cov_type = 'HAC', cov_kwds = {'maxlags':5} )
print(results.summary())



#=================
#Linear Regression with daily excess returns
#=================

#Daily return
last_prize = vix_p['PX_LAST'].array
dates_daily = vix_p['DATES'].tolist()
dates_daily = dates_daily[2:] 
#last_prize = vix_p['PX_LAST'].tolist()

xr = last_prize[2:]/last_prize[1:-1] -1 

vix_hat = vix_p['FORECAST'].array
#vix_hat = vix_p['FORECAST'].tolist()

last_prize_t = vix_p['PX_LAST'].array 
days_to_mat = vix_p['DAYS_TO_MATURITY']

#vixr_2 = (vix_hat[:-2]/last_prize_t[1:-1])**(1/days_to_mat[:-2]) -1 #Cheng uses VIXR-2 to estimate xr

vixr_daily = (vix_hat[:-2]/last_prize_t[:-2])**(1/days_to_mat[:-2]) -1 #Cheng uses VIXR-2 to estimate xr

X = sm.add_constant(vixr_daily)
Y = xr

model = sm.OLS(Y, X)
results = model.fit(cov_type = 'HAC', cov_kwds = {'maxlags':5} )
print(results.summary())

#the vixr_daily is already the t-2 vixr
df_daily = pd.DataFrame({'DATES': dates_daily, 'VIXR_DAILY_2' : vixr_daily})





#df_daily.to_csv('/Users/johannesthellmann/Desktop/vstoxx_daily.csv', index=False)
