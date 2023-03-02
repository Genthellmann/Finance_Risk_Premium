#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 24 15:18:18 2021

@author: johannesthellmann
"""



import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import datetime 

data_path =  '/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/data/csv/arma_2.csv'
cols_to_use = ['DATES','VIX','PX_BID','PX_ASK','PX_LAST','MATURITY','DAYS_TO_MATURITY','FORECAST','PREMIUM']
dtype_dic= {'DATES':str,'VIX':float,'PX_BID':float,'PX_ASK':float,'PX_LAST':float,'MATURITY':str,
            'DAYS_TO_MATURITY':float,'FORECAST':float, 'PREMIUM':float}
arma = pd.read_csv(data_path, sep=',', decimal='.', usecols=cols_to_use, dtype=dtype_dic)


#make date time object
arma['DATES_VIX'] = arma['DATES'] #Spalte ins Format to_datetime bringen
arma['DATES'] = pd.to_datetime(arma['DATES']) #Spalte ins Format to_datetime bringen
arma['MATURITY'] = pd.to_datetime(arma['MATURITY'])

#First future prizes from 2005-01-01, last from 2020-10-30
#cheng uses until end of may 2020

#Nur einen Zeitraum des Datensatzes verwenden, sonst start date von oben verwenden 
startdate = pd.to_datetime('2020-02-01')
enddate = pd.to_datetime('2020-05-22')
dates_to_use = (arma['DATES'] >= pd.to_datetime(startdate)) & (arma['DATES'] < pd.to_datetime(enddate))
arma = arma.loc[dates_to_use]



future_prize = arma['PX_LAST'].tolist()

#next day futures prize change
def nextdaychange(dataset, start=0):
	diff = []
	for i in range(start, len(dataset)-1):
		value = dataset[i+1] - dataset[i]
		diff.append(value)
	return np.array(diff)


fut_next = nextdaychange(future_prize)
arma.drop(arma.tail(1).index,inplace=True) # drop last n rows
arma['FUT_CHANGE'] = fut_next

#========================
#plot Zeitraum feb-may
#========================

#Nur einen Zeitraum des Datensatzes verwenden, sonst start date von oben verwenden 
startdate1 = pd.to_datetime('2020-02-01')
enddate1 = pd.to_datetime('2020-06-01')

#y-Werte
mask_plot1 = (arma['DATES'] > pd.to_datetime(startdate1)) & (arma['DATES'] < pd.to_datetime(enddate1))
arma_plot1 = arma.loc[mask_plot1]

#plot
fig = plt.figure(figsize=[8, 6]); # Set dimensions for figure
ax = fig.add_subplot()
 
#line
x = arma_plot1['DATES']
y = arma_plot1['PREMIUM']
ax.plot(x,y, label='VIXP')

#scatter
y = arma_plot1['FUT_CHANGE']
ax.scatter(x,y, marker = 'D', c = 'orange', label='Preisänderung')

ax.axhline(y=0, color='k') #show 0 level


ticks = pd.to_datetime(['2020-02-01', '2020-03-01','2020-04-01','2020-05-01'])
ax.set_xticks(ticks)
ax.set_xticklabels(['Feb 01', 'Mar 01','Apr 01', 'May 01'])

plt.legend(loc=2)
#plt.savefig('/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/results/VIXP.png', bbox_inches = 'tight')


#=================
#Linear Regression of tomorrows futures prize changes on tomorrows premium
#=================

import statsmodels.api as sm

#Für February through may verwenden
startdate = pd.to_datetime('2020-02-01')
enddate = pd.to_datetime('2020-05-21')
dates_ols = (arma['DATES'] >= pd.to_datetime(startdate)) & (arma['DATES'] <= pd.to_datetime(enddate))
arma_ols = arma.loc[dates_ols]


X = sm.add_constant(arma_ols['PREMIUM'])
Y = arma_ols['FUT_CHANGE']

model = sm.OLS(Y, X)
results = model.fit()
print(results.summary())


#=================
#to_excel
#=================
path_sp500 = '/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/data/csv/SP500.csv'
cols_to_use = ['Dates','PX_LAST']
dtype_dic= {'Dates':str,'PX_LAST':float}
sp500 = pd.read_csv(path_sp500, usecols=cols_to_use, dtype=dtype_dic)
sp500['index'] = sp500['Dates']

sp500 = sp500.set_index(sp500['index'])
sp500['SPX'] = sp500['PX_LAST']
sp500 = sp500.drop(['index', 'Dates','PX_LAST'], axis=1)

arma['index'] = arma['DATES_VIX']
arma = arma.set_index(arma['index'])

ex = pd.concat([sp500, arma], axis =1)

startdate_ex = pd.to_datetime('2020-02-12')
enddate_ex = pd.to_datetime('2020-06-01')
mask_ex = (ex['DATES'] >= pd.to_datetime(startdate_ex)) & (ex['DATES'] < pd.to_datetime(enddate_ex))
ex = ex.loc[mask_ex]
ex['Date'] = ex['DATES'].dt.strftime('%b %d (%a)')
ex['Maturity'] = ex['MATURITY'].dt.strftime('%b %d')
ex =ex.sort_values(by='DATES')
ex['Price'] = ex['PX_LAST']
ex['Fcast.'] = ex['FORECAST']
ex['VIXP'] = ex['PREMIUM']


ex= ex.drop(['DATES', 'PX_BID','PX_LAST', 'PX_ASK','FORECAST','DAYS_TO_MATURITY','MATURITY', 'PREMIUM', 'DATES_VIX', 'FUT_CHANGE','index'], axis = 1)

ex = ex[['Date', 'SPX','VIX','Price','Fcast.','VIXP', 'Maturity']]


#ex.to_excel('/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/results/results.xlsx', sheet_name = 'VIXP', index = False, float_format="%.2f")



