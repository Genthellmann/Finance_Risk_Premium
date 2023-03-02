#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 09:54:18 2021

@author: johannesthellmann
"""


import matplotlib.pyplot as plt
import pandas as pd


data_path =  '/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/data/csv/arma_2.csv'
#Anmerkung: Die hier verwendete ARMA.csv unterscheidet sich von der in vix_arma.py erzeugten arma.csv insofern, dass fehlerhafte Future-Werte (falsche Stelle des Dezimalpunktes)
#und das Premium für diese Werte
cols_to_use = ['DATES','VIX','PX_BID','PX_ASK','PX_LAST','MATURITY','DAYS_TO_MATURITY','FORECAST','PREMIUM']
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


#===========================
#Premium neu berechnen, aufgrund angepasster .csv file
vix_p['PREMIUM'] = vix_p['PX_LAST'] - vix_p['FORECAST']
#===========================

#==========================
#Data with correct EOM values
#==========================

data_path1 =  '/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/data/csv/vix_f_EOM_2.csv'
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
vix_eom['PX_ASK_EOM'] = vix_eom['PX_ASK']
vix_eom['PX_BID_EOM'] = vix_eom['PX_BID']

vix_eom['MATURITY_EOM'] = vix_eom['Maturity']
vix_eom['MATURITY_EOM'] = pd.to_datetime(vix_eom['MATURITY_EOM'])

vix_eom = vix_eom.drop(['CURRENT_CONTRACT_MONTH_YR', 'LAST_PRICE', 'PX_BID', 'PX_ASK', 'PX_LAST', 'Dates', 'Maturity'], axis = 1)


#concatenate vix_p and vix_eom
vix_p = pd.concat([vix_p, vix_eom], axis=1)

#Premium t-2
vixp = vix_p['PREMIUM'].tolist()
vixp_t_2 = vix_p['PREMIUM'].tolist()
vixp_t_2[0] = 0
vixp_t_2[1] = 0
vixp_t_2[2:] = vixp[:-2] 

#PX_BID-1
px_bid = vix_p['PX_BID'].tolist()
px_bid_1 = vix_p['PX_BID']
px_bid[0] = 0 
px_bid[1:] = px_bid[:-1] 

#PX_ASK t-1
px_ask = vix_p['PX_ASK'].tolist()
px_ask[0] = 0 
px_ask[1:] = px_ask[:-1] 

#PX_BID-1 EOM
px_bid_EOM = vix_p['PX_BID_EOM'].tolist()
px_bid_EOM[0] = 0 
px_bid_EOM[1:] = px_bid_EOM[:-1] 

#PX_ASK t-1 EOM
px_ask_EOM = vix_p['PX_ASK_EOM'].tolist()
px_ask_EOM[0] = 0 
px_ask_EOM[1:] = px_ask_EOM[:-1] 

#Add to Dataframe as new columns
vix_p['PREMIUM_T-2'] = vixp_t_2
vix_p['PX_BID-1'] = px_bid
vix_p['PX_ASK-1'] = px_ask
vix_p['PX_BID-1_EOM'] = px_bid_EOM
vix_p['PX_ASK-1_EOM'] = px_ask_EOM

vix_p['RETURN'] = 0
vix_p['CUM_RETURN'] = 0


#Nur einen Zeitraum des Datensatzes verwenden
startdate = pd.to_datetime('2020-02-01')
enddate = pd.to_datetime('2020-05-21')
dates_to_use = (vix_p['DATES'] >= pd.to_datetime(startdate)) & (vix_p['DATES'] < pd.to_datetime(enddate))
vix_p = vix_p.loc[dates_to_use]


return_t = [0 for i in range(len(vix_p))]
dates_t = ['' for j in range(len(vix_p))]


df_result = vix_p

indicator = True #indicator for fist period long/short/cash



for index, row in vix_p.iterrows():
    #indicator to show whether premium is positiv or negativ in t-2
    indicator = row['PREMIUM_T-2'] < 0
    
    print(indicator)
    
    if row['MATURITY'] != row['MATURITY_EOM']:
        if indicator == True:
            day_return = (row['PX_BID']/row['PX_ASK-1_EOM'] - 1)
            df_result.loc[index, 'RETURN'] = day_return
        if indicator == False:
            day_return =  -(row['PX_ASK']/row['PX_BID-1_EOM'] -1)
            df_result.loc[index, 'RETURN'] = day_return
        #print('EOM')
    
    elif indicator == True:
        day_return = (row['PX_BID']/row['PX_ASK-1'] - 1)
        df_result.loc[index, 'RETURN'] = day_return
        
    
    else:
        day_return =  -(row['PX_ASK']/row['PX_BID-1'] -1)
        df_result.loc[index, 'RETURN'] = day_return
    
        
    
df_result['CUM_RETURN'] = (df_result['RETURN'] + 1).cumprod() -1
    
    
    


#plot
fig = plt.figure(figsize=[15, 7.5]); # Set dimensions for figure
ax = fig.add_subplot()
x = df_result['DATES']
#y = return_t
y = df_result['CUM_RETURN']*100
ax.plot(x,y)
ax.axhline(y=0, color='k') #show 0 level
ticks = pd.to_datetime(['2020-02-01', '2020-03-01','2020-04-01','2020-05-01', '2020-06-01'])
ax.set_xticks(ticks)
ax.set_xticklabels(['Feb 01', 'Mar 01','Apr 01', 'May 01', 'Jun 01'])
    

