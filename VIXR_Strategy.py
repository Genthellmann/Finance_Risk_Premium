#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 11:14:03 2021

@author: johannesthellmann
"""

import pandas as pd

import matplotlib.pyplot as plt
import pandas as pd


def position_strategy(vixp, start, end, strat):
    start, end = pd.to_datetime(start), pd.to_datetime(end)
    result = pd.DataFrame(columns=['POS','CON','INDICATOR','RETURN','CUM_RETURN'], index = vixp.index[pd.to_datetime(vixp.index) > pd.to_datetime(start)])
    int_start = vixp.index.get_loc(vixp.index[pd.to_datetime(vixp.index) >= start][0])
    period1 = True
    
    for t2, t1, t in zip(vixp.index[(int_start-2):-2], vixp.index[(int_start-1):-1], vixp.index[int_start:]):        
        if pd.to_datetime(t) > end:
            break
        #indicator to show whether in period1 or period2 and to respective action long/short/cash
        indicator = vixp.loc[t, 'VIXR_DAILY_2'] > 0 #use vixr_daily of t since it already is the t-2 return
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
                result.loc[t, 'RETURN'] = (future_nm.loc[t, 'PX_BID'] / future_cm.loc[t1, 'PX_ASK_TS']-1) 
                result.loc[t, 'POS'] = 'L'
                result.loc[t, 'CON'] = future_nm.loc[t, 'MATURITY']
            if action == "S":
                result.loc[t, 'RETURN'] = -(future_nm.loc[t, 'PX_ASK']/ future_cm.loc[t1, 'PX_BID_TS'] -1) 
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

# ================================
# Data Prep
# ================================

data_path =  '/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/data/csv/arma_2.csv'
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
#Premium neu berechnen, aufgrund angepasster .csv file
vix_p['PREMIUM'] = vix_p['PX_LAST'] - vix_p['FORECAST']
#===========================

data_path1 = '/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/data/csv/vix_f_TS.csv'
#Anmerkung: Die hier verwendete ARMA.csv unterscheidet sich von der in vix_arma.py erzeugten arma.csv insofern, dass fehlerhafte Future-Werte (falsche Stelle des Dezimalpunktes)
#und das Premium für diese Werte
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

data_path2 = '/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/data/csv/vixr_daily.csv'
cols_to_use = ['DATES','VIXR_DAILY_2']
dtype_dic= {'DATES':str, 'VIX_R':float}
vix_r = pd.read_csv(data_path2, sep=',', decimal='.', usecols=cols_to_use, dtype=dtype_dic)
vix_r['INDEX'] = vix_r['DATES']
vix_r = vix_r.set_index(vix_r['INDEX'])
vix_r = vix_r.drop(['INDEX'], axis=1)
vix_r['DATES_VIXR'] = vix_r['DATES']
vix_r = vix_r.drop(['DATES'], axis = 1)

#concatenate vix_p and vix_eom
vix_p = pd.concat([vix_p, vix_p_ts, vix_r], axis=1)

vix_p = vix_p.dropna(subset=['PX_BID', 'PX_ASK'])

# ================================
# Trading Positions
# ================================
res_ls = position_strategy(vixp = vix_p, start = '2005-01-03', end = '2020-06-01', strat="L/S")



fig = plt.figure(figsize=[15, 7.5]); # Set dimensions for figure
ax = fig.add_subplot()
x  = pd.to_datetime(res_ls.index)
#y = return_t
y  = res_ls['CUM_RETURN']
ax.plot(x,y)
ax.axhline(y=0, color='k') #show 0 level
#ticks = pd.to_datetime(['2020-02-01', '2020-03-01','2020-04-01','2020-05-01', '2020-06-01'])
#ax.set_xticks(ticks)
#ax.set_xticklabels(['Feb 01', 'Mar 01','Apr 01', 'May 01', 'Jun 01'])


#res_ls.to_csv('/Users/johannesthellmann/Desktop/LS_TradingStrategy.csv', index=True) #index are the dates







