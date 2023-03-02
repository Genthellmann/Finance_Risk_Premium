#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 14:57:32 2021

@author: johannesthellmann
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import datetime 
import warnings
import statsmodels.api as sm


data_path =  '/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/data/csv/arma_2.csv'
cols_to_use = ['DATES','VIX','PX_BID','PX_ASK','PX_LAST','MATURITY','DAYS_TO_MATURITY','FORECAST','PREMIUM']
dtype_dic= {'DATES':str,'VIX':float,'PX_BID':float,'PX_ASK':float,'PX_LAST':float,'MATURITY':str,
            'DAYS_TO_MATURITY':float,'FORECAST':float, 'PREMIUM':float}
vix_p = pd.read_csv(data_path, sep=',', decimal='.', usecols=cols_to_use, dtype=dtype_dic)
vix_p['INDEX'] = vix_p['DATES']
vix_p = vix_p.set_index(vix_p['INDEX'])
vix_p = vix_p.drop(['INDEX'], axis=1)

#make date time object
vix_p['DATES'] = pd.to_datetime(vix_p['DATES']) #Spalte ins Format to_datetime bringen
vix_p['MATURITY'] = pd.to_datetime(vix_p['MATURITY'])

#VVIX Data
data_path1 = '/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/data/csv/VVIX.csv'
cols_to_use1 = ['Dates', 'PX_LAST']
dtype_dic1 = {'Dates':str, 'PX_LAST':float}
vvix = pd.read_csv(data_path1, sep=',', decimal='.', usecols=cols_to_use1)
vvix['INDEX'] = vvix['Dates']
vvix = vvix.set_index(vvix['INDEX'])
vvix = vvix.drop(['INDEX'], axis=1)
vvix['Dates_VVIX'] = pd.to_datetime(vvix['Dates']) #Spalte ins Format to_datetime bringen
vvix['PX_LAST_VVIX'] = vvix['PX_LAST']
vvix = vvix.drop(['PX_LAST'], axis=1)

#concatenate vix_p and vix_eom
vix_p = pd.concat([vix_p, vvix], axis=1)

# #Nur einen Zeitraum des Datensatzes verwenden, sonst start date von oben verwenden 
# startdate = pd.to_datetime('2020-02-01')
# enddate = pd.to_datetime('2020-05-22')
# dates_to_use = (vix_p['DATES'] >= pd.to_datetime(startdate)) & (vix_p['DATES'] < pd.to_datetime(enddate))
# vix_p = vix_p.loc[dates_to_use]

mask_isna = vix_p['PX_LAST_VVIX'].isna()
vix_p = vix_p.dropna(subset=['PX_LAST_VVIX'])


# #====================
# #Plot VIXP and market risk
# #====================

#Nur einen Zeitraum des Datensatzes verwenden, sonst start date von oben verwenden 
startdate = pd.to_datetime('2020-02-01')
enddate = pd.to_datetime('2020-05-22')
dates_to_use = (vix_p['DATES'] >= pd.to_datetime(startdate)) & (vix_p['DATES'] < pd.to_datetime(enddate))
vix_plot = vix_p.loc[dates_to_use]

mask_isna = vix_plot['PX_LAST_VVIX'].isna()
vix_plot = vix_plot.dropna(subset=['PX_LAST_VVIX'])

fig = plt.figure(figsize=[16, 9]); # Set dimensions for figure
ax1 = fig.add_subplot()

color = 'tab:red'
#ax1.set_ylabel('VIXP')
ax1.plot(vix_plot['DATES'], vix_plot['PREMIUM'], label = 'VIXP')
ax1.tick_params(axis='y')
ax1.set_ylim([-20, 50])

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

#ax2.set_ylabel('VIX, VVIX')  # we already handled the x-label with ax1
ax2.plot(vix_plot['DATES'],vix_plot['VIX'], linestyle = 'dotted', label = 'VIX', color = 'black')
#ax2.plot(vix_plot['DATES'],vix_plot['PX_LAST_VVIX'], linestyle = 'dashed', label='VVIX', color = 'black')
ax2.set_ylim([-40,100])
ax2.tick_params(axis='y')

ax1.axhline(y=0, color='k') #show 0 level
ticks = pd.to_datetime(['2020-02-01', '2020-03-01','2020-04-01','2020-05-01'])
ax1.set_xticks(ticks)
ax1.set_xticklabels(['Feb 01', 'Mar 01','Apr 01', 'May 01'])

plt.legend(loc = 2)
fig.tight_layout()  # otherwise the right y-label is slightly clipped

plt.savefig('/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/Präsentation/VIXP and fin market risk.png', bbox_inches = 'tight')


# # #====================
# # #Plot VIXP History
# # #====================

# #GFC 
# startdate_gfc = pd.to_datetime('2008-09-01')
# enddate_gfc = pd.to_datetime('2008-12-31')
# dates_to_use_gfc = (vix_p['DATES'] >= pd.to_datetime(startdate_gfc)) & (vix_p['DATES'] < pd.to_datetime(enddate_gfc))
# vix_plot_gfc = vix_p.loc[dates_to_use_gfc]

# #H1N1
# startdate_h1 = pd.to_datetime('2009-03-01')
# enddate_h1 = pd.to_datetime('2009-07-31')
# dates_to_use_h1 = (vix_p['DATES'] >= pd.to_datetime(startdate_h1)) & (vix_p['DATES'] < pd.to_datetime(enddate_h1))
# vix_plot_h1 = vix_p.loc[dates_to_use_h1]

# #Ebola
# startdate_ebola = pd.to_datetime('2014-10-01')
# enddate_ebola = pd.to_datetime('2015-01-31')
# dates_to_use_ebola = (vix_p['DATES'] >= pd.to_datetime(startdate_ebola)) & (vix_p['DATES'] < pd.to_datetime(enddate_ebola))
# vix_plot_ebola = vix_p.loc[dates_to_use_ebola]

# #plot Covid
# fig = plt.figure(figsize=[12,9]); # Set dimensions for figure
# ax = fig.add_subplot()
# x  = list(range(0, len(vix_plot)))
# x1 = list(range(0, len(vix_plot_gfc)))
# x2 = list(range(0, len(vix_plot_h1)))
# x3 = list(range(0, len(vix_plot_ebola)))

# #y = return_t
# y  = vix_plot['PREMIUM']
# y1 = vix_plot_gfc['PREMIUM']
# y2 = vix_plot_h1['PREMIUM']
# y3 = vix_plot_ebola['PREMIUM']
# ax.plot(x,y, linewidth = 4)
# ax.plot(x1, y1, color = 'grey')
# ax.plot(x2, y2, color = 'grey')
# ax.plot(x3, y3, color = 'grey')
# ax.axhline(y=0, color='k') #show 0 level
# ticks = [0,20,40,60,80]
# ax.set_xticks(ticks)
# ax.set_xticklabels([0,20,40,60,80])
# ax.set_xlabel('Handelstage')

# plt.savefig('/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/results/History/History_Covid19.png', bbox_inches = 'tight')

# #plot GFC
# fig = plt.figure(figsize=[12,9]); # Set dimensions for figure
# ax = fig.add_subplot()
# x  = list(range(0, len(vix_plot)))
# x1 = list(range(0, len(vix_plot_gfc)))
# x2 = list(range(0, len(vix_plot_h1)))
# x3 = list(range(0, len(vix_plot_ebola)))

# #y = return_t
# y  = vix_plot['PREMIUM']
# y1 = vix_plot_gfc['PREMIUM']
# y2 = vix_plot_h1['PREMIUM']
# y3 = vix_plot_ebola['PREMIUM']
# ax.plot(x,y, color = 'grey')
# ax.plot(x1, y1, linewidth = 4)
# ax.plot(x2, y2, color = 'grey')
# ax.plot(x3, y3, color = 'grey')
# ax.axhline(y=0, color='k') #show 0 level
# ticks = [0,20,40,60,80]
# ax.set_xticks(ticks)
# ax.set_xticklabels([0,20,40,60,80])
# ax.set_xlabel('Handelstage')

# plt.savefig('/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/results/History/History_GFC.png', bbox_inches = 'tight')

# #plot H1N1
# fig = plt.figure(figsize=[12,9]); # Set dimensions for figure
# ax = fig.add_subplot()
# x  = list(range(0, len(vix_plot)))
# x1 = list(range(0, len(vix_plot_gfc)))
# x2 = list(range(0, len(vix_plot_h1)))
# x3 = list(range(0, len(vix_plot_ebola)))

# #y = return_t
# y  = vix_plot['PREMIUM']
# y1 = vix_plot_gfc['PREMIUM']
# y2 = vix_plot_h1['PREMIUM']
# y3 = vix_plot_ebola['PREMIUM']
# ax.plot(x,y, color = 'grey')
# ax.plot(x1, y1, color='grey')
# ax.plot(x2, y2, linewidth = 4)
# ax.plot(x3, y3, color = 'grey')
# ax.axhline(y=0, color='k') #show 0 level
# ticks = [0,20,40,60,80]
# ax.set_xticks(ticks)
# ax.set_xticklabels([0,20,40,60,80])
# ax.set_xlabel('Handelstage')

# plt.savefig('/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/results/History/History_H1N1.png', bbox_inches = 'tight')


# #plot Ebola
# fig = plt.figure(figsize=[12,9]); # Set dimensions for figure
# ax = fig.add_subplot()
# x  = list(range(0, len(vix_plot)))
# x1 = list(range(0, len(vix_plot_gfc)))
# x2 = list(range(0, len(vix_plot_h1)))
# x3 = list(range(0, len(vix_plot_ebola)))

# #y = return_t
# y  = vix_plot['PREMIUM']
# y1 = vix_plot_gfc['PREMIUM']
# y2 = vix_plot_h1['PREMIUM']
# y3 = vix_plot_ebola['PREMIUM']
# ax.plot(x,y, color = 'grey')
# ax.plot(x1, y1, color = 'grey')
# ax.plot(x2, y2, color = 'grey')
# ax.plot(x3, y3, linewidth = 4)
# ax.axhline(y=0, color='k') #show 0 level
# ticks = [0,20,40,60,80]
# ax.set_xticks(ticks)
# ax.set_xticklabels([0,20,40,60,80])
# ax.set_xlabel('Handelstage')

# plt.savefig('/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/results/History/History_Ebola.png', bbox_inches = 'tight')



































