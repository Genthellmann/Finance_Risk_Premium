#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 14:52:37 2021

@author: johannesthellmann
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import datetime 
import warnings
from scipy.stats import skew
from scipy.stats import kurtosis


data_path =  '/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/data/csv/eurostoxx_arma.csv'
#Anmerkung: Die hier verwendete ARMA.csv unterscheidet sich von der in vix_arma.py erzeugten arma.csv insofern, dass fehlerhafte Future-Werte (falsche Stelle des Dezimalpunktes)
#und das Premium für diese Werte
cols_to_use = ['DATES', 'PX_LAST', 'PX_BID', 'PX_ASK', 'FORECAST','MATURITY', 'PREMIUM']
dtype_dic= {'DATES':str, 'PX_LAST':float,'PX_BID':float, 'PX_ASK':float, 'MATURITY':str, 'FORECAST':float, 'PREMIUM':float}
vix_p = pd.read_csv(data_path, sep=',', decimal='.', usecols=cols_to_use, dtype=dtype_dic)

#Index erstellen zuerst als extra Spalte dann als index und behalten für differenz zu maturity date
vix_p['INDEX'] = vix_p['DATES']
vix_p = vix_p.set_index(vix_p['INDEX'])
vix_p = vix_p.drop(['INDEX'], axis=1)

#make date time object
vix_p['DATES'] = pd.to_datetime(vix_p['DATES']) #Spalte ins Format to_datetime bringen

#===========================
#Data with corrected End of Month future prize
#===========================

data_path1 = '/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/data/csv/eurostoxx_eom.csv'
cols_to_use = ['Dates','PX_BID','PX_ASK','Maturity']
dtype_dic= {'Dates':str,'PX_BID':float,'PX_ASK':float,'Maturity':str}
vix_p_ts = pd.read_csv(data_path1, sep=',', decimal='.', usecols=cols_to_use, dtype=dtype_dic)

#Index erstellen zuerst als extra Spalte dann als index und behalten für differenz zu maturity date
vix_p_ts['INDEX'] = vix_p_ts['Dates']
vix_p_ts = vix_p_ts.set_index(vix_p_ts['INDEX'])
vix_p_ts = vix_p_ts.drop(['INDEX'], axis=1)

#make date time object
vix_p_ts['Dates'] = pd.to_datetime(vix_p_ts['Dates']) #Spalte ins Format to_datetime bringen
vix_p_ts['PX_BID_TS'] = vix_p_ts['PX_BID']
vix_p_ts['PX_ASK_TS'] = vix_p_ts['PX_ASK']
vix_p_ts = vix_p_ts.drop(['PX_BID'], axis=1)
vix_p_ts = vix_p_ts.drop(['PX_ASK'], axis=1)


vix_p = pd.concat([vix_p, vix_p_ts], axis = 1)


def position_strategy(vixp, start, end, strat):
    
    start, end = pd.to_datetime(start), pd.to_datetime(end)
    result = pd.DataFrame(columns=['POS','CON','INDICATOR','RETURN','CUM_RETURN'], index = vixp.index[pd.to_datetime(vixp.index) > pd.to_datetime(start)])
    int_start = vixp.index.get_loc(vixp.index[pd.to_datetime(vixp.index) >= start][0])
    period1 = True
    

    
    for t2, t1, t in zip(vixp.index[(int_start-2):-2], vixp.index[(int_start-1):-1], vixp.index[int_start:]):

        # t2 = vixp.index[(int_start-2):-2]
        # t1 = vixp.index[(int_start-1):-1]
        # t = vixp.index[int_start:]
        # strat = "L/S"
        
        # t2 = t2[0]
        # t1 = t1[0]
        # t = t[0]
            
        
        if pd.to_datetime(t) > end:
            break
        #indicator to show whether in period1 or period2 and to respective action long/short/cash
        indicator = vixp.loc[t2, 'PREMIUM'] < 0
        
        result.loc[t, 'INDICATOR'] = "L" if indicator else "S"
        #which action to perform for period1 and period2
        action = strat.split("/")[0] if indicator else strat.split("/")[1]
        
        #roll the position at the end of the month
        cur_mat = vixp.loc[t1, 'MATURITY']        #maturity t-1
        next_mat = vixp.loc[t, 'MATURITY']        #maturity t 
        future_cm = vixp[vixp['MATURITY'] == cur_mat] #prizes of futures for current maturity
        future_nm = vixp[vixp['MATURITY'] == next_mat] #prizes of futures for next maturity
                
        if cur_mat != next_mat:
            if action == 'L':
                result.loc[t, 'RETURN'] = (future_nm.loc[t, 'PX_BID'] / future_cm.loc[t1, 'PX_ASK_TS']-1) #Hier verwendet MB future next maturity
                result.loc[t, 'POS'] = 'L'
                result.loc[t, 'CON'] = future_nm.loc[t, 'MATURITY']
            if action == "S":
                result.loc[t, 'RETURN'] = -(future_nm.loc[t, 'PX_ASK']/ future_cm.loc[t1, 'PX_BID_TS'] -1) #Hier verwendet MB future next maturity
                result.loc[t, 'POS'] = 'S'
                result.loc[t, 'CON'] = future_nm.loc[t, 'MATURITY']
            if action == "C":
                result.loc[t, 'RETURN'] = 0
                result.loc[t, 'POS'] = 'C'
                result.loc[t, 'CON'] = 'C'
        elif period1 or action != result.loc[t1, 'POS']:
            period1 = False
            if action == "L":
                result.loc[t, 'RETURN'] = (future_cm.loc[t, 'PX_BID'] / future_cm.loc[t1, 'PX_ASK']-1)
                result.loc[t, 'POS'] = 'L'
                result.loc[t, 'CON'] = future_cm.loc[t, 'MATURITY']
            if action == "S":
                result.loc[t, 'RETURN'] = -(future_cm.loc[t, 'PX_ASK'] / future_cm.loc[t1, 'PX_BID'] -1)
                result.loc[t, 'POS'] = 'S'
                result.loc[t, 'CON'] = future_cm.loc[t, 'MATURITY']
            if action == "C":
                result.loc[t, 'RETURN'] = 0
                result.loc[t, 'POS'] = 'C'
                result.loc[t, 'CON'] = 'C'
        else:
            result.loc[t, 'POS'] = result.loc[t1, 'POS']
            result.loc[t, 'RETURN'] = 0 if result.loc[t, 'POS'] == "C" else ((future_cm.loc[t, 'PX_BID'] / future_cm.loc[t1, 'PX_BID'] - 1)  if result.loc[t, 'POS'] == "L" else -(future_cm.loc[t, 'PX_ASK'] / future_cm.loc[t1, 'PX_ASK'] - 1))
            result.loc[t, 'CON'] = result.loc[t1, 'CON']

        
    result = result[pd.to_datetime(result.index) <= end]
        
    result['CUM_RETURN'] = (result['RETURN'] + 1).cumprod() - 1
    return result.copy()

        
res_lc = position_strategy(vixp = vix_p, start = '2020-01-25', end = '2020-05-21', strat = "L/C") 
res_cs = position_strategy(vixp = vix_p, start = '2020-01-25', end = '2020-05-21', strat = "C/S")    
res_ls = position_strategy(vixp = vix_p, start = '2020-01-25', end = '2020-05-21', strat = "L/S")    
res_ss = position_strategy(vixp = vix_p, start = '2020-01-25', end = '2020-05-21', strat = "S/S")    
res_ss = position_strategy(vixp = vix_p, start = '2020-01-25', end = '2020-05-21', strat = "S/S")    

#Alternative Handelsstrategien nicht von Cheng
res_ll = position_strategy(vixp = vix_p, start = '2020-01-25', end = '2020-05-21', strat = "L/L")    
res_sc = position_strategy(vixp = vix_p, start = '2020-01-25', end = '2020-05-21', strat = "S/C")    
res_sl = position_strategy(vixp = vix_p, start = '2020-01-25', end = '2020-05-21', strat = "S/L")    
res_cl = position_strategy(vixp = vix_p, start = '2020-01-25', end = '2020-05-21', strat = "C/L")    

        
#plot1
fig = plt.figure(figsize=[8, 6]); # Set dimensions for figure
ax = fig.add_subplot()
x  = pd.to_datetime(res_lc.index)
x1 = pd.to_datetime(res_cs.index)
x2 = pd.to_datetime(res_ls.index)
x3 = pd.to_datetime(res_ss.index)

#y = return_t
y  = res_lc['CUM_RETURN']*100
y1 = res_cs['CUM_RETURN']*100
y2 = res_ls['CUM_RETURN']*100
y3 = res_ss['CUM_RETURN']*100
ax.plot(x,y, linewidth = 4)
ax.plot(x1, y1, color = 'grey')
ax.plot(x2, y2, color = 'grey')
ax.plot(x3, y3, color='grey')
ax.set_ylim([-100,350])
ax.axhline(y=0, color='k') #show 0 level
ticks = pd.to_datetime(['2020-02-01', '2020-03-01','2020-04-01','2020-05-01'])
ax.set_xticks(ticks)
ax.set_xticklabels(['Feb 01', 'Mar 01','Apr 01', 'May 01'])  
#ax.set_title('Long/Cash')   
#plt.savefig('/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/results/Trading Strategies Europe/TS_EURO_LC.png', bbox_inches = 'tight')

#plot2
fig = plt.figure(figsize=[4,3]); # Set dimensions for figure
ax = fig.add_subplot()
x  = pd.to_datetime(res_lc.index)
x1 = pd.to_datetime(res_cs.index)
x2 = pd.to_datetime(res_ls.index)
x3 = pd.to_datetime(res_ss.index)

#y = return_t
y  = res_lc['CUM_RETURN']*100
y1 = res_cs['CUM_RETURN']*100
y2 = res_ls['CUM_RETURN']*100
y3 = res_ss['CUM_RETURN']*100
ax.plot(x,y, color = 'grey')
ax.plot(x1, y1, linewidth = 4)
ax.plot(x2, y2, color = 'grey')
ax.plot(x3, y3, color='grey')
ax.set_ylim([-100,350])
ax.axhline(y=0, color='k') #show 0 level
ticks = pd.to_datetime(['2020-02-01', '2020-03-01','2020-04-01','2020-05-01'])
ax.set_xticks(ticks)
ax.set_xticklabels(['Feb 01', 'Mar 01','Apr 01', 'May 01'])  
#ax.set_title('Cash/Short')   
#plt.savefig('/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/results/Trading Strategies Europe/TS_EURO_CS.png', bbox_inches = 'tight')
 

#plot3
fig = plt.figure(figsize=[4,3]); # Set dimensions for figure
ax = fig.add_subplot()
x  = pd.to_datetime(res_lc.index)
x1 = pd.to_datetime(res_cs.index)
x2 = pd.to_datetime(res_ls.index)
x3 = pd.to_datetime(res_ss.index)

#y = return_t
#y  = res_lc['CUM_RETURN']*100
#y1 = res_cs['CUM_RETURN']*100
y2 = res_ls['CUM_RETURN']*100
y3 = res_ss['CUM_RETURN']*100
#ax.plot(x,y, color = 'grey')
#ax.plot(x1, y1, color = 'grey')
ax.plot(x2, y2, linewidth = 4)
ax.plot(x3, y3, color='grey')
ax.set_ylim([-100,350])
ax.axhline(y=0, color='k') #show 0 level
ticks = pd.to_datetime(['2020-02-01', '2020-03-01','2020-04-01','2020-05-01'])
ax.set_xticks(ticks)
ax.set_xticklabels(['Feb 01', 'Mar 01','Apr 01', 'May 01'])   
#ax.set_title('Long/Short')   
plt.savefig('/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/Präsentation/TSEUROLS.pdf',bbox_inches = 'tight')


#plot
fig = plt.figure(figsize=[4,3]); # Set dimensions for figure
ax = fig.add_subplot()
x  = pd.to_datetime(res_lc.index)
x1 = pd.to_datetime(res_cs.index)
x2 = pd.to_datetime(res_ls.index)
x3 = pd.to_datetime(res_ss.index)

#y = return_t
#y  = res_lc['CUM_RETURN']*100
#y1 = res_cs['CUM_RETURN']*100
y2 = res_ls['CUM_RETURN']*100
y3 = res_ss['CUM_RETURN']*100
#ax.plot(x,y, color = 'grey')
#ax.plot(x1, y1, color = 'grey')
ax.plot(x2, y2, color = 'grey')
ax.plot(x3, y3, linewidth = 4)
ax.set_ylim([-100,350])
ax.axhline(y=0, color='k') #show 0 level
ticks = pd.to_datetime(['2020-02-01', '2020-03-01','2020-04-01','2020-05-01'])
ax.set_xticks(ticks)
ax.set_xticklabels(['Feb 01', 'Mar 01','Apr 01', 'May 01'])
#ax.set_title('Short/Short')   
plt.savefig('/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/Präsentation/TSEUROSS.pdf', bbox_inches = 'tight')
  

#============================
#Alernative Handelsstrategien nicht von Cheng
#============================
#plot 5
fig = plt.figure(figsize=[8,6]); # Set dimensions for figure
ax = fig.add_subplot()
x  = pd.to_datetime(res_ll.index)
x1 = pd.to_datetime(res_sc.index)
x2 = pd.to_datetime(res_sl.index)
x3 = pd.to_datetime(res_cl.index)

#y = return_t
y  = res_ll['CUM_RETURN']*100
y1 = res_sc['CUM_RETURN']*100
y2 = res_sl['CUM_RETURN']*100
y3 = res_cl['CUM_RETURN']*100
ax.plot(x,y, linewidth = 4)
ax.plot(x1, y1, color = 'grey')
ax.plot(x2, y2, color = 'grey')
ax.plot(x3, y3, color = 'grey')
ax.set_ylim([-100,350])
ax.axhline(y=0, color='k') #show 0 leve
ticks = pd.to_datetime(['2020-02-01', '2020-03-01','2020-04-01','2020-05-01'])
ax.set_xticks(ticks)
ax.set_xticklabels(['Feb 01', 'Mar 01','Apr 01', 'May 01'])
#ax.set_title('long/long')   
#plt.savefig('/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/results/Trading Strategies Europe/TS_EURO_LL.png', bbox_inches = 'tight')

#plot 6
fig = plt.figure(figsize=[8,6]); # Set dimensions for figure
ax = fig.add_subplot()
x  = pd.to_datetime(res_ll.index)
x1 = pd.to_datetime(res_sc.index)
x2 = pd.to_datetime(res_sl.index)
x3 = pd.to_datetime(res_cl.index)

#y = return_t
y  = res_ll['CUM_RETURN']*100
y1 = res_sc['CUM_RETURN']*100
y2 = res_sl['CUM_RETURN']*100
y3 = res_cl['CUM_RETURN']*100
ax.plot(x,y, color = 'grey')
ax.plot(x1, y1, linewidth = 4)
ax.plot(x2, y2, color = 'grey')
ax.plot(x3, y3, color = 'grey')
ax.set_ylim([-100,350])
ax.axhline(y=0, color='k') #show 0 level
ticks = pd.to_datetime(['2020-02-01', '2020-03-01','2020-04-01','2020-05-01'])
ax.set_xticks(ticks)
ax.set_xticklabels(['Feb 01', 'Mar 01','Apr 01', 'May 01'])
#ax.set_title('short/cash')   
#plt.savefig('/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/results/Trading Strategies Europe/TS_EURO_SC.png', bbox_inches = 'tight')

#plot 7
fig = plt.figure(figsize=[8,6]); # Set dimensions for figure
ax = fig.add_subplot()
x  = pd.to_datetime(res_ll.index)
x1 = pd.to_datetime(res_sc.index)
x2 = pd.to_datetime(res_sl.index)
x3 = pd.to_datetime(res_cl.index)

#y = return_t
y  = res_ll['CUM_RETURN']*100
y1 = res_sc['CUM_RETURN']*100
y2 = res_sl['CUM_RETURN']*100
y3 = res_cl['CUM_RETURN']*100
ax.plot(x,y, color = 'grey')
ax.plot(x1, y1, color = 'grey')
ax.plot(x2, y2, linewidth = 4)
ax.plot(x3, y3, color = 'grey')
ax.set_ylim([-100,350])
ax.axhline(y=0, color='k') #show 0 level
ticks = pd.to_datetime(['2020-02-01', '2020-03-01','2020-04-01','2020-05-01'])
ax.set_xticks(ticks)
ax.set_xticklabels(['Feb 01', 'Mar 01','Apr 01', 'May 01'])
#ax.set_title('short/long')   
#plt.savefig('/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/results/Trading Strategies Europe/TS_EURO_SL.png', bbox_inches = 'tight')



#plot 8
fig = plt.figure(figsize=[8,6]); # Set dimensions for figure
ax = fig.add_subplot()
x4  = pd.to_datetime(res_ll.index)
x5 = pd.to_datetime(res_sc.index)
x6 = pd.to_datetime(res_sl.index)
x7 = pd.to_datetime(res_cl.index)

#y = return_t

y4  = res_ll['CUM_RETURN']*100
y5 = res_sc['CUM_RETURN']*100
y6 = res_sl['CUM_RETURN']*100
y7 = res_cl['CUM_RETURN']*100
ax.plot(x4,y4, color = 'grey')
ax.plot(x5, y5, color = 'grey')
ax.plot(x6, y6, color = 'grey')
ax.plot(x7, y7,  linewidth = 4)
ax.set_ylim([-100,350])
ax.axhline(y=0, color='k') #show 0 level
ticks = pd.to_datetime(['2020-02-01', '2020-03-01','2020-04-01','2020-05-01'])
ax.set_xticks(ticks)
ax.set_xticklabels(['Feb 01', 'Mar 01','Apr 01', 'May 01'])
#ax.set_title('cash/long')   
#plt.savefig('/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/results/Trading Strategies Europe/TS_EURO_CL.png', bbox_inches = 'tight')

#plot 9
fig = plt.figure(figsize=[8,6]); # Set dimensions for figure
ax = fig.add_subplot()
x  = pd.to_datetime(res_lc.index)
x1 = pd.to_datetime(res_cs.index)
x2 = pd.to_datetime(res_ls.index)
x3 = pd.to_datetime(res_ss.index)
x4  = pd.to_datetime(res_ll.index)
x5 = pd.to_datetime(res_sc.index)
x6 = pd.to_datetime(res_sl.index)
x7 = pd.to_datetime(res_cl.index)

#y = return_t
y  = res_lc['CUM_RETURN']*100
y1 = res_cs['CUM_RETURN']*100
y2 = res_ls['CUM_RETURN']*100
y3 = res_ss['CUM_RETURN']*100
y4  = res_ll['CUM_RETURN']*100
y5 = res_sc['CUM_RETURN']*100
y6 = res_sl['CUM_RETURN']*100
y7 = res_cl['CUM_RETURN']*100
ax.plot(x,y, color = 'grey', label = 'long/cash')
ax.plot(x1, y1, color = 'black', label = 'cash/short')
ax.plot(x2, y2, color = 'blue', label= 'long/short')
ax.plot(x3, y3,  color = 'royalblue', label= 'short/short')
ax.plot(x4,y4, color = 'navy', label= 'long/long')
ax.plot(x5, y5, color = 'mediumpurple', label= 'short/cash')
ax.plot(x6, y6, color = 'darkorchid', label='short/long')
ax.plot(x7, y7,  color = 'dodgerblue', label = 'cash/long')
ax.set_ylim([-100,350])
ax.axhline(y=0, color='k') #show 0 level
ticks = pd.to_datetime(['2020-02-01', '2020-03-01','2020-04-01','2020-05-01'])
ax.set_xticks(ticks)
ax.set_xticklabels(['Feb 01', 'Mar 01','Apr 01', 'May 01'])
#ax.set_title('Übersicht Handelsstrategien')   
plt.legend(loc=2)
#plt.savefig('/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/results/Trading Strategies Europe/TS_EURO_Uebersicht.png', bbox_inches = 'tight')


#summary table for threshold Strategien

path_sp500 = '/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/data/csv/EuroStoxx_index.csv'
cols_to_use = ['DATES','PX_LAST']
dtype_dic= {'DATES':str,'PX_LAST':float}
sp500 = pd.read_csv(path_sp500, usecols=cols_to_use, dtype=dtype_dic)
sp500['index'] = sp500['DATES']

sp500['DATES'] = pd.to_datetime(sp500['DATES'])
dates_to_use = (sp500['DATES']>=pd.to_datetime('2020-01-25'))&(sp500['DATES']<=pd.to_datetime('2020-05-21'))
sp500 =  sp500.loc[dates_to_use]

sp500 = sp500.set_index(sp500['index'])
sp500['SPX'] = sp500['PX_LAST']
sp500 = sp500.drop(['index', 'DATES','PX_LAST'], axis=1)

#excess return sp500
spx = sp500['SPX'].array
sp_excess = (spx[1:]/spx[:-1] -1)*100


#calculate summary table for threshod trading
lc  = res_lc['RETURN']*100
cs = res_cs['RETURN']*100
ls = res_ls['RETURN']*100
ss = res_ss['RETURN']*100
ll  = res_ll['RETURN']*100
sc = res_sc['RETURN']*100
sl = res_sl['RETURN']*100
cl = res_cl['RETURN']*100

strat = [lc, ls, ll, cs, ss, sc, sl, cl]

col_name = ['Mean','SD','Skew','Kurt','5%','50%','95%','T']
summary = pd.DataFrame(columns = col_name)

summary = summary.append({'Mean' : np.mean(sp_excess),'SD' : np.std(sp_excess), 'Skew' : skew(sp_excess),
                           'Kurt' : kurtosis(sp_excess), '5%' : np.quantile(sp_excess, 0.05), '50%' : np.quantile(sp_excess, 0.5),
                           '95%' : np.quantile(sp_excess, 0.95), 'T' : len(sp_excess)}, ignore_index=True)
                       

for s in strat:
    mean = s.mean()
    sd = s.std()
    skew = s.skew()
    kurt = s.kurtosis()
    five = s.quantile(0.05)
    fifty = s.quantile(0.5)
    ninetyfive = s.quantile(0.95)
    T = s.count()
    
    summary = summary.append({'Mean' : mean, 'SD' : sd, 'Skew' : skew, 'Kurt' : kurt, '5%' : five,'50%' : fifty, '95%' : ninetyfive, 'T' : T}, ignore_index=True)
    
  
#summary.to_excel('/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/results/results_TS_euro.xlsx', sheet_name = 'TS_SUM', index = False, float_format="%.2f")



#res_ls.to_csv('/Users/johannesthellmann/Desktop/LS_Euro.csv')
