#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 16:29:06 2021

@author: johannesthellmann
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data_path =  '/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/data/csv/eurostoxx_arma.csv'
#Anmerkung: Die hier verwendete ARMA.csv unterscheidet sich von der in vix_arma.py erzeugten arma.csv insofern, dass fehlerhafte Future-Werte (falsche Stelle des Dezimalpunktes)
#und das Premium für diese Werte
cols_to_use = ['DATES','ES','PX_BID','PX_ASK','PX_LAST','MATURITY','DAYS_TO_MATURITY','FORECAST','PREMIUM']
dtype_dic= {'DATES':str,'ES':float,'PX_BID':float,'PX_ASK':float,'PX_LAST':float,'MATURITY':str,
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

#cases
data_path_covid = '/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/data/csv/eurostoxx_cases.csv'
cols_to_use = ['DATE', 'SUM_CASES']
dtype_dic= {'DATE':str,'SUM_CASES':float}
covid = pd.read_csv(data_path_covid, sep=',', decimal='.', usecols=cols_to_use, dtype=dtype_dic)
covid['INDEX'] = covid['DATE']
covid = covid.set_index(covid['INDEX'])
covid = covid.drop(['INDEX'], axis=1)
covid['DATE'] = pd.to_datetime(covid['DATE']) #Spalte ins Format to_datetime bringen
covid['cases'] = covid['SUM_CASES']
covid = covid.drop(['SUM_CASES'], axis=1)
covid['cases'].fillna(0, inplace = True)

#deaths
data_path_covid = '/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/data/csv/eurostoxx_deaths.csv'
cols_to_use = ['DATE', 'SUM_DEATHS']
dtype_dic= {'DATE':str,'SUM_CASES':float}
deaths = pd.read_csv(data_path_covid, sep=',', decimal='.', usecols=cols_to_use, dtype=dtype_dic)
deaths['INDEX'] = deaths['DATE']
deaths = deaths.set_index(deaths['INDEX'])
deaths = deaths.drop(['INDEX'], axis=1)
deaths['DATE'] = pd.to_datetime(deaths['DATE']) #Spalte ins Format to_datetime bringen
deaths['deaths'] = deaths['SUM_DEATHS']
deaths = deaths.drop(['SUM_DEATHS'], axis=1)
deaths = deaths.drop(['DATE'], axis=1)
deaths['deaths'].fillna(0, inplace = True)

covid = pd.concat([covid, deaths], axis = 1)

covid = covid.sort_values(by = 'DATE')

covid['cases'] = covid['cases'].fillna(0)
covid['deaths'] = covid['deaths'].fillna(0)



covid['cases_cum'] = covid['cases'].cumsum()
covid['deaths_cum'] = covid['deaths'].cumsum()


covid['growth_rate_cases'] = 0
covid['growth_rate_deaths'] = 0
for t in range(7, covid.shape[0]):
    covid.iloc[t, 5] = np.log(covid.iloc[(t-6):t]['cases_cum'].sum()) - np.log(covid.iloc[(t - 7):(t-1)]['cases_cum'].sum())
    covid.iloc[t, 6] = np.log(covid.iloc[(t-6):t]['deaths_cum'].sum()) - np.log(covid.iloc[(t - 7):(t-1)]['deaths_cum'].sum())



#period VIXP
startdate = pd.to_datetime('2020-02-01')
enddate = pd.to_datetime('2020-05-22')
covid_period = ((vix_p['DATES'] >=startdate) & (vix_p['DATES'] < enddate))
vix_p = vix_p.loc[covid_period]

#period cases
covid_period = (covid['cases'] > 100)
covid_cases = covid.loc[covid_period]

startdate = pd.to_datetime('2020-01-25')
enddate = pd.to_datetime('2020-05-22')
covid_period = ((covid_cases['DATE'] >=startdate) & (covid_cases['DATE'] < enddate))
covid_cases = covid_cases.loc[covid_period]

#period deaths
covid_period = (covid['deaths'] > 100)
covid_deaths = covid.loc[covid_period]
startdate = pd.to_datetime('2020-01-25')
enddate = pd.to_datetime('2020-05-22')
covid_period = ((covid_deaths['DATE'] >=startdate) & (covid_deaths['DATE'] < enddate))
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
ax = fig.add_subplot()
x = vix_p['DATES']
y = vix_p['PREMIUM']
x1 = covid_cases['DATE']
x2 = covid_deaths['DATE']
y3=vix_p['ES']

y_change = vix_p['FUT_CHANGE']
ax.scatter(x,y_change, marker = 'D', c = 'black', label='Preisänderung')


y1 = covid_cases['growth_rate_cases']*100
y2 = covid_deaths['growth_rate_deaths'] *100
ax.plot(x,y, label = 'VSTOXXP', linewidth = 4)
ax.plot(x1, y1, color = 'black', linestyle = 'dashed', label = 'Cases', linewidth = 4)
ax.plot(x2, y2, color = 'grey', linestyle = 'dotted', label = 'Deaths', linewidth = 4)
ax.axhline(y=0, color='k') #show 0 level
# ticks = pd.to_datetime(['2020-02-01', '2020-03-01','2020-04-01','2020-05-01'])
# ax.set_xticks(ticks)
# ax.set_xticklabels(['Feb 01', 'Mar 01','Apr 01', 'May 01'], fontsize = 18)
ax.tick_params(axis='y', labelsize=22)
ax.set_ylim([-20,50])
#plt.legend(loc=2)
#ax.plot(x,y3/2, linestyle = 'dotted', label = 'VSTOXX', color = 'orange')
# plt.legend(loc=2, fontsize = 18)
ax2 = ax.twinx()  # instantiate a second axes that shares the same x-axis
#ax2.set_ylabel('VIX, VVIX')  # we already handled the x-label with ax1
#ax2.plot(x,y3, linestyle = 'dotted', label = 'VIX', color = 'orange')

ax2.plot(x,y3, linestyle = 'dotted', label = 'VSTOXX', color = 'orange', linewidth = 4)
ax2.set_ylim([-40,100])
ax2.tick_params(axis='y', labelsize = 22)

lines_1, labels_1 = ax.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()

lines = lines_1 + lines_2
labels = labels_1 + labels_2

plt.legend(lines, labels, loc=0, fontsize=22)
ticks = pd.to_datetime(['2020-02-01', '2020-03-01','2020-04-01','2020-05-01'])
ax.set_xticks(ticks)
ax.set_xticklabels(['Feb 01', 'Mar 01','Apr 01', 'May 01'], fontsize = 22)

#plt.legend(loc=2, fontsize = 18)

plt.savefig('/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/Präsentation/eurostoxx_cases_deaths.pdf', bbox_inches = 'tight')





