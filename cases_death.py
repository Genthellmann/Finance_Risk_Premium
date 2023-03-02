#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 16:16:04 2021

@author: johannesthellmann
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data_path =  '/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/data/csv/arma_2.csv'
#Anmerkung: Die hier verwendete ARMA.csv unterscheidet sich von der in vix_arma.py erzeugten arma.csv insofern, dass fehlerhafte Future-Werte (falsche Stelle des Dezimalpunktes)
#und das Premium für diese Werte
cols_to_use = ['DATES','VIX','PX_BID','PX_ASK','PX_LAST','MATURITY','DAYS_TO_MATURITY','FORECAST','PREMIUM']
dtype_dic= {'DATES':str,'VIX':float,'PX_BID':float,'PX_ASK':float,'PX_LAST':float,'MATURITY':str,
            'DAYS_TO_MATURITY':float,'FORECAST':float, 'PREMIUM':float}
vix_p = pd.read_csv(data_path, sep=',', decimal='.', usecols=cols_to_use, dtype=dtype_dic)
vix_p['INDEX'] = vix_p['DATES']
vix_p = vix_p.set_index(vix_p['INDEX'])
vix_p = vix_p.drop(['INDEX'], axis=1)
vix_p['DATES'] = pd.to_datetime(vix_p['DATES']) #Spalte ins Format to_datetime bringen
vix_p['MATURITY'] = pd.to_datetime(vix_p['MATURITY'])

#==================
#covid data
#==================

data_path_covid = '/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/data/csv/covid.csv'
cols_to_use = ['date', 'cases', 'deaths']
dtype_dic= {'date':str,'cases':float,'deaths':float}
covid = pd.read_csv(data_path_covid, sep=',', decimal='.', usecols=cols_to_use, dtype=dtype_dic)
covid['INDEX'] = covid['date']
covid = covid.set_index(covid['INDEX'])
covid = covid.drop(['INDEX'], axis=1)
covid['date_covid'] = pd.to_datetime(covid['date']) #Spalte ins Format to_datetime bringen
covid = covid.drop(['date'], axis=1)

covid['cases'].fillna(0, inplace = True)
covid['deaths'].fillna(0, inplace = True)


# covid['cases_new'] = covid['cases'].pct_change()
# covid['deaths_new'] = covid['deaths'].pct_change()

covid['growth_rate_cases'] = 0
covid['growth_rate_deaths'] = 0
for t in range(7, covid.shape[0]):
    covid.iloc[t, 3] = np.log(covid.iloc[(t-6):t]['cases'].sum()) - np.log(covid.iloc[(t - 7):(t-1)]['cases'].sum())
    covid.iloc[t, 4] = np.log(covid.iloc[(t-6):t]['deaths'].sum()) - np.log(covid.iloc[(t - 7):(t-1)]['deaths'].sum())



#period VIXP
startdate = pd.to_datetime('2020-02-01')
enddate = pd.to_datetime('2020-05-22')
covid_period = ((vix_p['DATES'] >=startdate) & (vix_p['DATES'] < enddate))
vix_p = vix_p.loc[covid_period]

#period cases
covid_period = (covid['cases'] > 100)
covid_cases = covid.loc[covid_period]

startdate = pd.to_datetime('2020-02-01')
enddate = pd.to_datetime('2020-05-22')
covid_period = ((covid_cases['date_covid'] >=startdate) & (covid_cases['date_covid'] < enddate))
covid_cases = covid_cases.loc[covid_period]

#period deaths
covid_period = (covid['deaths'] > 100)
covid_deaths = covid.loc[covid_period]
startdate = pd.to_datetime('2020-02-01')
enddate = pd.to_datetime('2020-05-22')
covid_period = ((covid_deaths['date_covid'] >=startdate) & (covid_deaths['date_covid'] < enddate))
covid_deaths = covid_deaths.loc[covid_period]

future_prize = vix_p['PX_LAST'].tolist()

#next day futures prize change
def nextdaychange(dataset, start=0):
	diff = []
	for i in range(start, len(dataset)-1):
		value = dataset[i+1] - dataset[i]
		diff.append(value)
	return np.array(diff)


fut_next = nextdaychange(future_prize)
vix_p.drop(vix_p.tail(1).index,inplace=True) # drop last n rows
vix_p['FUT_CHANGE'] = fut_next


#plot
fig = plt.figure(figsize=[16, 9]); 
ax1 = fig.add_subplot()
x = vix_p['DATES']
y = vix_p['PREMIUM']
y3 = vix_p['VIX']
x1 = covid_cases['date_covid']
x2 = covid_deaths['date_covid']

y_change = vix_p['FUT_CHANGE']
ax1.scatter(x,y_change, marker = 'D', c = 'black', label='Preisänderung')

y1 = covid_cases['growth_rate_cases']*100
y2 = covid_deaths['growth_rate_deaths'] *100
ax1.plot(x,y, label = 'VIXP', linewidth = 4)
ax1.plot(x1, y1, color = 'black', linestyle = 'dashed', label = 'Cases', linewidth = 4)
ax1.plot(x2, y2, color = 'grey', linestyle = 'dotted', label = 'Deaths', linewidth = 4)
ax1.axhline(y=0, color='k') #show 0 level
ticks = pd.to_datetime(['2020-02-01', '2020-03-01','2020-04-01','2020-05-01'])
ax1.set_xticks(ticks)
ax1.set_xticklabels(['Feb 01', 'Mar 01','Apr 01', 'May 01'], fontsize = 22)
ax1.tick_params(axis='y', labelsize=22)
ax1.set_ylim([-20,50])

ax1.plot(x,y3/2, linestyle = 'dotted', label = 'VIX', color = 'orange', linewidth = 4)
plt.legend(loc=0, fontsize = 22)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
#ax2.set_ylabel('VIX, VVIX')  # we already handled the x-label with ax1
#ax2.plot(x,y3, linestyle = 'dotted', label = 'VIX', color = 'orange')

#ax2.plot(vix_plot['DATES'],vix_plot['PX_LAST_VVIX'], linestyle = 'dashed', label='VVIX', color = 'black')
ax2.set_ylim([-40,100])
ax2.tick_params(axis='y', labelsize = 22)



plt.savefig('/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/Präsentation/cases_deaths.pdf', bbox_inches = 'tight')



