#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 27 19:05:00 2021

@author: johannesthellmann
"""


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import datetime 
import warnings
import statsmodels.api as sm

#VIX
data_path =  '/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/data/csv/arma_2.csv'
cols_to_use = ['DATES','PREMIUM']
dtype_dic= {'DATES':str,'PREMIUM':float}
vix_p = pd.read_csv(data_path, sep=',', decimal='.', usecols=cols_to_use, dtype=dtype_dic)
vix_p['INDEX'] = vix_p['DATES']
vix_p['VIXP'] = vix_p['PREMIUM']
vix_p = vix_p.set_index(vix_p['INDEX'])
vix_p = vix_p.drop(['INDEX'], axis=1)

#make date time object
vix_p['DATES_VIX'] = pd.to_datetime(vix_p['DATES']) #Spalte ins Format to_datetime bringen
vix_p = vix_p.drop(['DATES'], axis=1)
vix_p = vix_p.drop(['PREMIUM'], axis=1)



#VSTOXX

data_path1 =  '/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/data/csv/eurostoxx_arma.csv'
cols_to_use = ['DATES','PREMIUM']
dtype_dic= {'DATES':str, 'PREMIUM':float}
vstoxx_p = pd.read_csv(data_path1, sep=',', decimal='.', usecols=cols_to_use, dtype=dtype_dic)
vstoxx_p['INDEX'] = vstoxx_p['DATES']
vstoxx_p['VSTOXXP'] = vstoxx_p['PREMIUM']
vstoxx_p = vstoxx_p.set_index(vstoxx_p['INDEX'])
vstoxx_p = vstoxx_p.drop(['INDEX'], axis=1)
vstoxx_p['DATES_VSTOXX'] = pd.to_datetime(vstoxx_p['DATES']) #Spalte ins Format to_datetime bringen
vstoxx_p = vstoxx_p.drop(['DATES'], axis=1)
vstoxx_p = vstoxx_p.drop(['PREMIUM'], axis=1)



concat = pd.concat([vix_p, vstoxx_p], axis = 1)
concat = concat.dropna()


# #====================
# #Plot VIXP History
# #====================

#covid
startdate_cov = pd.to_datetime('2020-02-01')
enddate_cov = pd.to_datetime('2020-06-01')
dates_to_use_cov = (concat['DATES_VSTOXX'] >= pd.to_datetime(startdate_cov)) & (concat['DATES_VSTOXX'] < pd.to_datetime(enddate_cov))
concatlot_cov = concat.loc[dates_to_use_cov]

#GFC 
startdate_gfc = pd.to_datetime('2008-09-01')
enddate_gfc = pd.to_datetime('2008-12-29')
dates_to_use_gfc = (concat['DATES_VSTOXX'] >= pd.to_datetime(startdate_gfc)) & (concat['DATES_VSTOXX'] < pd.to_datetime(enddate_gfc))
concatlot_gfc = concat.loc[dates_to_use_gfc]

#H1N1
startdate_h1 = pd.to_datetime('2009-03-01')
enddate_h1 = pd.to_datetime('2009-07-31')
dates_to_use_h1 = (concat['DATES_VSTOXX'] >= pd.to_datetime(startdate_h1)) & (concat['DATES_VSTOXX'] < pd.to_datetime(enddate_h1))
concatlot_h1 = concat.loc[dates_to_use_h1]

#Ebola
startdate_ebola = pd.to_datetime('2014-10-01')
enddate_ebola = pd.to_datetime('2015-01-30')
dates_to_use_ebola = (concat['DATES_VSTOXX'] >= pd.to_datetime(startdate_ebola)) & (concat['DATES_VSTOXX'] < pd.to_datetime(enddate_ebola))
concatlot_ebola = concat.loc[dates_to_use_ebola]

#Brexit
startdate_brexit = pd.to_datetime('2016-05-01')
enddate_brexit = pd.to_datetime('2016-08-24')
dates_to_use_brexit= (concat['DATES_VSTOXX'] >= pd.to_datetime(startdate_brexit)) & (concat['DATES_VSTOXX'] < pd.to_datetime(enddate_brexit))
concatlot_brexit = concat.loc[dates_to_use_brexit]

#plot Covid
fig = plt.figure(figsize=[4,3]); # Set dimensions for figure
ax = fig.add_subplot()
x1  = list(range(0, len(concatlot_cov)))

#y = return_t
y1  = concatlot_cov['VIXP']
y2 = concatlot_cov['VSTOXXP']
ax.plot(x1,y1,  label = 'VIXP')
ax.plot(x1, y2, label = 'VSTOXXP')
ax.axhline(y=0, color='k') #show 0 level
ticks = [0,20,40,60,80]
ax.set_xticks(ticks)
ax.set_xticklabels([0,20,40,60,80])
#ax.set_xlabel('Handelstage')
ax.set_ylim([-20, 5])
plt.legend(loc = 3)

plt.savefig('/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/Präsentation/both_History_covid.pdf', bbox_inches = 'tight')

#plot GFC
fig = plt.figure(figsize=[4,3]); # Set dimensions for figure
ax = fig.add_subplot()

x1 = list(range(0, len(concatlot_gfc)))
y1 = concatlot_gfc['VIXP']
ax.plot(x1, y1, label = 'VIXP')
ax.axhline(y=0, color='k') #show 0 level
ticks = [0,20,40,60,80]
ax.set_xticks(ticks)
ax.set_xticklabels([0,20,40,60,80])
#ax.set_xlabel('Handelstage')
ax.set_ylim([-20, 5])
plt.legend(loc = 3)

plt.savefig('/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/Präsentation/both_History_GFC.pdf', bbox_inches = 'tight')

#plot Brexit
fig = plt.figure(figsize=[4,3]); # Set dimensions for figure
ax = fig.add_subplot()

x1 = list(range(0, len(concatlot_brexit)))
y1 = concatlot_brexit['VIXP']
y2 = concatlot_brexit['VSTOXXP']
ax.plot(x1, y1, label = 'VIXP')
ax.plot(x1, y2, label = 'VSTOXXP')
ax.axhline(y=0, color='k') #show 0 level
ticks = [0,20,40,60,80]
ax.set_xticks(ticks)
ax.set_xticklabels([0,20,40,60,80])
#ax.set_xlabel('Handelstage')
ax.set_ylim([-20,5])
plt.legend(loc = 3)

plt.savefig('/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/Präsentation/both_History_Brexit.pdf', bbox_inches = 'tight')


#plot Ebola
fig = plt.figure(figsize=[4,3]); # Set dimensions for figure
ax = fig.add_subplot()
x3 = list(range(0, len(concatlot_ebola)))

#y = return_t

y1 = concatlot_ebola['VIXP']
y2 = concatlot_ebola['VSTOXXP']

ax.plot(x3,y1, label = 'VIXP')
ax.plot(x3, y2, label = 'VSTOXXP')

ax.axhline(y=0, color='k') #show 0 level
ticks = [0,20,40,60,80]
ax.set_xticks(ticks)
ax.set_xticklabels([0,20,40,60,80])
#ax.set_xlabel('Handelstage')
ax.set_ylim([-20,5])
plt.legend(loc = 3)




plt.savefig('/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/Präsentation/both_History_Ebola.pdf', bbox_inches = 'tight')