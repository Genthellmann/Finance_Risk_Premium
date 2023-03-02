#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 21:53:23 2021

@author: johannesthellmann
"""


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import datetime 
import holidays
#from datetime import date

#partial auto corr
from statsmodels.tsa.stattools import pacf
#autocorr
from statsmodels.tsa.stattools import acf
#plot of partial auto corr
from statsmodels.graphics.tsaplots import plot_pacf
#plot of auto corr
from statsmodels.graphics.tsaplots import plot_acf
#ARMA
#from statsmodels.tsa.arima_model import ARMA

#ARIMA
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import adfuller

from pandas.tseries.holiday import USFederalHolidayCalendar
from pandas.tseries.offsets import CustomBusinessDay

#====================================
#data vix futures
#====================================
data_path =  '/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/data/csv/eurostoxx.csv'
cols_to_use = ['Dates', 'CURRENT_CONTRACT_MONTH_YR', 'LAST_PRICE', 'PX_BID','PX_ASK', 'PX_LAST', 'Maturity']
dtype_dic= {'Dates':str,'CURRENT_CONTRACT_MONTH_YR':str, 'LAST_PRICE':float, 'PX_BID':float, 'PX_ASK': float, 'PX_LAST':float, 'Maturity': str}
vix_f = pd.read_csv(data_path, sep=',', decimal='.', usecols=cols_to_use, dtype=dtype_dic)

#Index erstellen zuerst als extra Spalte dann als index und behalten für differenz zu maturity date
vix_f['index'] = vix_f['Dates']
vix_f = vix_f.set_index(vix_f['index'])
vix_f = vix_f.drop(['index'], axis=1)

#make date time object
vix_f['Dates'] = pd.to_datetime(vix_f['Dates']) #Spalte ins Format to_datetime bringen
vix_f['Maturity'] = pd.to_datetime(vix_f['Maturity'])

#clean data
#drop rows with missing dates
vix_f.dropna(subset=["Dates"], inplace=True)

#Caculate number of days to Maturity
#Extract US Holidays
us_holidays = []
for date in holidays.UnitedStates(years=[1990,1991,1992,1993,1994,1995,1996,1997,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021]).items():
    us_holidays.append(date[0])
    
#create numpy busdaycalendar
us_bd = np.busdaycalendar(weekmask='1111100', holidays = us_holidays )
#Calculate Number of Days
A = [d.date() for d in vix_f['Dates']]
B = [d.date() for d in vix_f['Maturity']]
#vix_f['DELTA'] = np.busday_count(A, B, busdaycal=us_bd)
vix_f['DAYS_TO_MATURITY'] = np.busday_count(A, B, weekmask = '1111100', holidays = us_holidays)

#====================================
#data vix vix_s
#====================================

data_path =  '/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/data/csv/Vstoxx.csv'
cols_to_use = ['Dates', 'PX_LAST']
dtype_dic= {'Dates':str,'PX_LAST':float}
vix_s = pd.read_csv(data_path, sep=',', decimal='.', usecols=cols_to_use, dtype=dtype_dic)

#Index erstellen zuerst als extra Spalte
vix_s['index'] = vix_s['Dates']
vix_s = vix_s.set_index(vix_s['index'])
vix_s = vix_s.drop(['index'], axis=1)

vix_s['Dates'] = pd.to_datetime(vix_s['Dates']) #Spalte ins Format to_datetime bringen

#Rename columns to avoid ambiguity
vix_s['Dates_VIX'] = vix_s['Dates'] 
vix_s = vix_s.drop(['Dates'], axis=1)
vix_s['VIX'] = vix_s['PX_LAST'] 
vix_s = vix_s.drop(['PX_LAST'], axis=1)

#clean data
#drop rows with missing dates
vix_s.dropna(subset=['Dates_VIX'], inplace=True)

#concatenate vix and vix futures
vix = pd.concat([vix_s, vix_f], axis=1)

vix = vix.drop(['CURRENT_CONTRACT_MONTH_YR'], axis = 1)

#drop rows with VIX is na
vix.dropna(subset=['Dates_VIX'], inplace=True)

# #return row with nan
# mask_isna = vix_f['PX_LAST'].isna()
# df_isna = vix_f.loc[mask_isna]

month = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
#month = ['MAY']
year = [ '04','05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20','21']
#year = ['04']


#make index as range
vix['index'] = range(0,len(vix))
vix = vix.set_index(vix['index'])
vix = vix.drop(['index'], axis=1)


#Spalte für Forecast
vix['FORECAST'] = 0

#Spalte für VIX Premium
vix['PREMIUM'] = 0

#Calculate VIX Premium for time period
startdate = '2009-12-01'
enddate = '2021-05-06'
start_date = vix[vix['Dates']==pd.to_datetime(startdate)].index.values.astype(int)[0]
end_date = vix[vix['Dates']==pd.to_datetime(enddate)].index.values.astype(int)[0]
print('startdate: ' + str(start_date) + '\n' + 'enddate: ' + str(end_date))

#===========================
#Hier noch kurze Schleife,falls Tag nicht verfügbar ist
#===========================



#Iteriere dataframe und schätze VIX aus vorhergehenden Tagen mit ARMA
#Erster Tag für den VIX Future vorliegt ist 01. Dezember 2004 mit Index 3758
for i in range(start_date, end_date):
    #Training Data until yesterday
    t_data = vix.loc[0:i-1] #oder i
    
    #todays observation
    today_obs = vix.loc[i:i] #oder i
    
    #model
    t_model = ARIMA(t_data['VIX'], order=(2, 0, 2))
    t_results = t_model.fit()
        
    #one/multi-step out of sample forecast
    #The result of the forecast() function is an array containing the forecast value [0], the standard error [1] of the forecast, and the confidence interval information
    days_to_maturity = int(vix.loc[i, ['DAYS_TO_MATURITY']].values[0])
    
    #Now append results for todays vix value...
    app_results =  t_results.append(today_obs.VIX, refit=False)
    
    #...and save in Forecast column
    vix.loc[i, ['FORECAST']]= app_results.forecast(steps=(days_to_maturity)).iloc[days_to_maturity-1]

    #VIX PREMIUM
    vix.loc[i, ['PREMIUM']] = (vix.loc[i, ['PX_LAST']].values[0] - vix.loc[i, ['FORECAST']].values[0])
    print(i)




#Drop unecessary cols before plot and csv
#davor einheitliche Spaltenbeschreibung
vix = vix.drop(['Dates'], axis=1)

vix['DATES'] = vix['Dates_VIX']
vix = vix.drop(['Dates_VIX'], axis=1)

vix['MATURITY'] = vix['Maturity']
vix = vix.drop(['Maturity'], axis=1)

vix = vix.drop(['LAST_PRICE'], axis=1)

#Order of columns
vix = vix[['DATES', 'VIX','PX_BID', 'PX_ASK', 'PX_LAST','MATURITY', 'DAYS_TO_MATURITY','FORECAST', 'PREMIUM']]


# #====================
# #Plot
# #====================

    
# #Nur einen Zeitraum des Datensatzes verwenden, sonst start date von oben verwenden 
# #start_date = pd.to_datetime('2020-02-03')
# #end_date = pd.to_datetime('2020-06-01')

# #y-Werte
# mask_plot = (vix['DATES'] > pd.to_datetime(startdate)) & (vix['DATES'] <= pd.to_datetime(enddate))
# vix_plot = vix.loc[mask_plot]

# #plot
# fig = plt.figure(figsize=[15, 7.5]); # Set dimensions for figure
# ax = fig.add_subplot()
# x = vix_plot['DATES']
# y = vix_plot['PREMIUM']
# ax.plot(x,y)
# ax.axhline(y=0, color='k') #show 0 level
# ticks = pd.to_datetime(['2020-02-01', '2020-03-01','2020-04-01','2020-05-01', '2020-06-01'])
# ax.set_xticks(ticks)
# ax.set_xticklabels(['Feb 01', 'Mar 01','Apr 01', 'May 01', 'Jun 01'])


#====================
#save to .csv
#====================

vix.to_csv('/Users/johannesthellmann/Desktop/eurostoxx_arma.csv', index=False)
