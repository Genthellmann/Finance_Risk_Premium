#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 10:16:58 2021

@author: johannesthellmann
"""

import pandas as pd
import numpy as np

path3 = '/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/data/csv/Europe_5_Factors_Daily.csv'
cols_to_use = ['Dates','Mkt-RF','SMB','HML','RMW','CMA','RF']
dict_type = {'Dates':str,'Mkt-RF':float,'SMB':float,'HML':float,'RMW':float,'CMA':float,'RF':float}
ff = pd.read_csv(path3, delimiter=',', decimal='.', usecols=cols_to_use, dtype=dict_type)
ff['INDEX'] = ff['Dates']
ff = ff.set_index(ff['INDEX'])
ff = ff.drop(['INDEX'], axis=1)
ff['Dates_FF'] = pd.to_datetime(ff['Dates'], format = '%Y%m%d')
ff = ff.drop(['Dates'], axis=1)

ff.to_csv('/Users/johannesthellmann/Desktop/ff_europe_daily.csv', index = False)
