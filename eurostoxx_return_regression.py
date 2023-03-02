#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 08:53:57 2021

@author: johannesthellmann
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import datetime 

data_path =  '/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/data/csv/eurostoxx_arma.csv'
cols_to_use = ['DATES','ES','PX_BID','PX_ASK','PX_LAST','MATURITY','DAYS_TO_MATURITY','FORECAST','PREMIUM']
dtype_dic= {'DATES':str,'ES':float,'PX_BID':float,'PX_ASK':float,'PX_LAST':float,'MATURITY':str,'DAYS_TO_MATURITY':float,'FORECAST':float,'PREMIUM':float}
es = pd.read_csv(data_path, sep=',', decimal='.', usecols=cols_to_use, dtype=dtype_dic)
es['index'] = es['DATES']
es = es.set_index(es['index'])
es = es.drop(['index'], axis=1)
es['DATES'] = pd.to_datetime(es['DATES']) #Spalte ins Format to_datetime bringen
es['MATURITY'] = pd.to_datetime(es['MATURITY'])

startdate = pd.to_datetime('2020-02-01')
enddate = pd.to_datetime('2020-05-22')
dates_to_use = (es['DATES'] >= pd.to_datetime(startdate)) & (es['DATES'] < pd.to_datetime(enddate))
es = es.loc[dates_to_use]


future_prize = es['PX_LAST'].tolist()

#next day futures prize change
def nextdaychange(dataset, start=0):
	diff = []
	for i in range(start, len(dataset)-1):
		value = dataset[i+1] - dataset[i]
		diff.append(value)
	return np.array(diff)

fut_next = nextdaychange(future_prize)
es.drop(es.tail(1).index,inplace=True)
es['FUT_CHANGE'] = fut_next

#plot
fig = plt.figure(figsize=[10, 5]); # Set dimensions for figure
ax = fig.add_subplot()

#line
x = es['DATES']
y = es['PREMIUM']
ax.plot(x,y, label='VSTOXXP')

#scatter
y = es['FUT_CHANGE']
ax.scatter(x,y, marker = 'D', c = 'orange', label='Preisänderung')

ax.axhline(y=0, color='k') #show 0 level

ticks = pd.to_datetime(['2020-02-01', '2020-03-01','2020-04-01','2020-05-01'])
ax.set_xticks(ticks)
ax.set_xticklabels(['Feb 01', 'Mar 01','Apr 01', 'May 01'])
plt.legend(loc=2)

plt.savefig('/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/Präsentation/VSTOXXP.pdf', bbox_inches = 'tight')



# #=================
# #Linear Regression of tomorrows futures prize changes on tomorrows premium
# #=================

import statsmodels.api as sm

#Für February through may verwenden
startdate = pd.to_datetime('2020-01-01')
enddate = pd.to_datetime('2020-05-21')
dates_ols = (es['DATES'] >= pd.to_datetime(startdate)) & (es['DATES'] <= pd.to_datetime(enddate))
arma_ols = es.loc[dates_ols]


X = sm.add_constant(arma_ols['PREMIUM'])
Y = arma_ols['FUT_CHANGE']

model = sm.OLS(Y, X)
results = model.fit()
print(results.summary())



#=================
#to_excel
#=================
path_sp500 = '/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/data/csv/EuroStoxx_index.csv'
cols_to_use = ['DATES','PX_LAST']
dtype_dic= {'DATES':str,'PX_LAST':float}
sp500 = pd.read_csv(path_sp500, usecols=cols_to_use, dtype=dtype_dic)
sp500['index'] = sp500['DATES']

sp500 = sp500.set_index(sp500['index'])
sp500['EUROSTOXX 50'] = sp500['PX_LAST']
sp500 = sp500.drop(['index', 'DATES','PX_LAST'], axis=1)

# es['index'] = es['DATES']
# es = es.set_index(es['index'])

ex = pd.concat([sp500, es], axis =1)

startdate_ex = pd.to_datetime('2020-01-25')
enddate_ex = pd.to_datetime('2020-06-01')
mask_ex = (ex['DATES'] >= pd.to_datetime(startdate_ex)) & (ex['DATES'] < pd.to_datetime(enddate_ex))
ex = ex.loc[mask_ex]
ex['Date'] = ex['DATES'].dt.strftime('%b %d (%a)')
ex['Maturity'] = ex['MATURITY'].dt.strftime('%b %d')
ex =ex.sort_values(by='DATES')
ex['Price'] = ex['PX_LAST']
ex['Fcast.'] = ex['FORECAST']
ex['VSTOXXP'] = ex['PREMIUM']
ex['VSTOXX'] = ex['ES']



ex= ex.drop(['DATES', 'ES', 'PX_BID','PX_LAST', 'PX_ASK','FORECAST','DAYS_TO_MATURITY','MATURITY', 'PREMIUM', 'FUT_CHANGE'], axis = 1)

ex = ex[['Date', 'EUROSTOXX 50','VSTOXX','Price','Fcast.','VSTOXXP', 'Maturity']]

#ex.to_excel('/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/results/results_euro.xlsx', sheet_name = 'EURO', index = False, float_format="%.2f")


