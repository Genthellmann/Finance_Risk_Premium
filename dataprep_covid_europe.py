#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 16:29:34 2021

@author: johannesthellmann
"""

import numpy as np
import pandas as pd

data_path_covid = '/Users/johannesthellmann/Desktop/SoSe2021/Seminar BWL/data/csv/data_worldwide.csv'
cols_to_use = ['dateRep','cases','deaths','countriesAndTerritories','continentExp']
dtype_dic= {'dateRep':str,'cases':float,'deaths':float, 'countriesAndTerritories':str,'continentExp':str}
covid = pd.read_csv(data_path_covid, sep=',', decimal='.', usecols=cols_to_use, dtype=dtype_dic)



# covid['date_covid'] = pd.to_datetime(covid['dateRep'], format='%d//m/%Y') 
# covid = covid.drop(['dateRep'], axis=1)



# #Austria
# mask_aut = covid['countriesAndTerritories'] == 'Austria'
# austria = covid.loc[mask_aut]
# austria = austria.set_index(['dateRep'])
# austria_cases = austria['cases'] 
# austria_deaths = austria['deaths'] 

#Belgium
mask_bel = covid['countriesAndTerritories'] == 'Belgium'
belgium = covid.loc[mask_bel]
belgium = belgium.set_index(['dateRep'])
belgium_cases = belgium['cases'] 
belgium_deaths = belgium['deaths'] 

# #bulgaria
# mask_bul = covid['countriesAndTerritories'] == 'Bulgaria'
# bulgaria = covid.loc[mask_bul]
# bulgaria = bulgaria.set_index(['dateRep'])
# bulgaria_cases = bulgaria['cases'] 
# bulgaria_deaths = bulgaria['deaths'] 

# #croatia
# mask_cro = covid['countriesAndTerritories'] == 'Croatia'
# croatia = covid.loc[mask_cro]
# croatia = croatia.set_index(['dateRep'])
# croatia_cases = croatia['cases'] 
# croatia_deaths = croatia['deaths'] 

# #Cyprus
# mask_cyp = covid['countriesAndTerritories'] == 'Cyprus'
# cyprus = covid.loc[mask_cyp]
# cyprus = cyprus.set_index(['dateRep'])
# cyprus_cases = cyprus['cases'] 
# cyprus_deaths = cyprus['deaths'] 

# #Czech
# mask_cze = covid['countriesAndTerritories'] == 'Czechia'
# czech = covid.loc[mask_cze]
# czech = czech.set_index(['dateRep'])
# czech_cases = czech['cases'] 
# czech_deaths = czech['deaths'] 

# #denmark
# mask_den = covid['countriesAndTerritories'] == 'Denmark'
# denmark = covid.loc[mask_den]
# denmark = denmark.set_index(['dateRep'])
# denmark_cases = denmark['cases'] 
# denmark_deaths = denmark['deaths'] 

# #estonia
# mask_est = covid['countriesAndTerritories'] == 'Estonia'
# estonia = covid.loc[mask_est]
# estonia = estonia.set_index(['dateRep'])
# estonia_cases = estonia['cases'] 
#estonia_deaths = estonia['deaths'] 

#finland
mask_fin = covid['countriesAndTerritories'] == 'Finland'
finland = covid.loc[mask_fin]
finland = finland.set_index(['dateRep'])
finland_cases = finland['cases'] 
finland_deaths = finland['deaths'] 

#france
mask_france = covid['countriesAndTerritories'] == 'France'
france = covid.loc[mask_france]
france = france.set_index(['dateRep'])
france_cases = france['cases'] 
france_deaths = france['deaths'] 

#Germany
mask_ger = covid['countriesAndTerritories'] == 'Germany'
germany = covid.loc[mask_ger]
germany = germany.set_index(['dateRep'])
germany_cases = germany['cases'] 
germany_deaths = germany['deaths'] 

# #Greece
# mask_gre = covid['countriesAndTerritories'] == 'Greece'
# greece = covid.loc[mask_gre]
# greece = greece.set_index(['dateRep'])
# greece_cases = greece['cases'] 
# greece_deaths = greece['deaths'] 

# #Hungary
# mask_hun = covid['countriesAndTerritories'] == 'Hungary'
# hungary = covid.loc[mask_hun]
# hungary = hungary.set_index(['dateRep'])
# hungary_cases = hungary['cases'] 
# hungary_deaths = hungary['deaths'] 

# #iceland
# mask_ice = covid['countriesAndTerritories'] == 'Iceland'
# iceland = covid.loc[mask_ice]
# iceland = iceland.set_index(['dateRep'])
# iceland_cases = iceland['cases'] 
# iceland_deaths = iceland['deaths'] 

#Ireland
mask_ire = covid['countriesAndTerritories'] == 'Ireland'
ireland = covid.loc[mask_ire]
ireland = ireland.set_index(['dateRep'])
ireland_cases = ireland['cases'] 
ireland_deaths = ireland['deaths'] 

#Italy
mask_it = covid['countriesAndTerritories'] == 'Italy'
italy = covid.loc[mask_it]
italy = italy.set_index(['dateRep'])
italy_cases = italy['cases'] 
italy_deaths = italy['deaths'] 

# #Latvia
# mask_lat= covid['countriesAndTerritories'] == 'Latvia'
# latvia = covid.loc[mask_lat]
# latvia = latvia.set_index(['dateRep'])
# latvia_cases = latvia['cases'] 
# latvia_deaths = latvia['deaths'] 

# #Liechtenstein
# mask_lie = covid['countriesAndTerritories'] == 'Liechtenstein'
# liechtenstein = covid.loc[mask_lie]
# liechtenstein = liechtenstein.set_index(['dateRep'])
# liechtenstein_cases = liechtenstein['cases'] 
# liechtenstein_deaths = liechtenstein['deaths'] 

# #Lithuania
# mask_lia = covid['countriesAndTerritories'] == 'Lithuania'
# lithuania = covid.loc[mask_lia]
# lithuania = lithuania.set_index(['dateRep'])
# lithuania_cases = lithuania['cases'] 
# lithuania_deaths = lithuania['deaths'] 

# #Luxembourg
# mask_lux = covid['countriesAndTerritories'] == 'Luxembourg'
# luxembourg = covid.loc[mask_lux]
# luxembourg = luxembourg.set_index(['dateRep'])
# luxembourg_cases = luxembourg['cases'] 
# luxembourg_deaths = luxembourg['deaths'] 

# #Malta
# mask_mal = covid['countriesAndTerritories'] == 'Malta'
# malta = covid.loc[mask_mal]
# malta = malta.set_index(['dateRep'])
# malta_cases = malta['cases'] 
# malta_deaths = malta['deaths'] 

#Netherlands
mask_net = covid['countriesAndTerritories'] == 'Netherlands'
netherlands = covid.loc[mask_net]
netherlands = netherlands.set_index(['dateRep'])
netherlands_cases = netherlands['cases'] 
netherlands_deaths = netherlands['deaths'] 

# #Norway
# mask_nor = covid['countriesAndTerritories'] == 'Norway'
# norway = covid.loc[mask_nor]
# norway = norway.set_index(['dateRep'])
# norway_cases = norway['cases'] 
# norway_deaths = norway['deaths'] 

# #Poland
# mask_pol = covid['countriesAndTerritories'] == 'Poland'
# poland = covid.loc[mask_pol]
# poland = poland.set_index(['dateRep'])
# poland_cases = poland['cases'] 
# poland_deaths = poland['deaths'] 

# #Portugal
# mask_por = covid['countriesAndTerritories'] == 'Portugal'
# portugal = covid.loc[mask_por]
# portugal = portugal.set_index(['dateRep'])
# portugal_cases = portugal['cases'] 
# portugal_deaths = portugal['deaths'] 

# #Romania
# mask_rom = covid['countriesAndTerritories'] == 'Romania'
# romania = covid.loc[mask_rom]
# romania = romania.set_index(['dateRep'])
# romania_cases = romania['cases'] 
# romania_deaths = romania['deaths'] 

# #Slovakia
# mask_slo = covid['countriesAndTerritories'] == 'Slovakia'
# slovakia = covid.loc[mask_slo]
# slovakia = slovakia.set_index(['dateRep'])
# slovakia_cases = slovakia['cases'] 
# slovakia_deaths = slovakia['deaths'] 

# #slovenia
# mask_sl = covid['countriesAndTerritories'] == 'Slovenia'
# slovenia = covid.loc[mask_sl]
# slovenia = slovenia.set_index(['dateRep'])
# slovenia_cases = slovenia['cases'] 
# slovenia_deaths = slovenia['deaths'] 

#spain
mask_spa = covid['countriesAndTerritories'] == 'Spain'
spain = covid.loc[mask_spa]
spain = spain.set_index(['dateRep'])
spain_cases = spain['cases'] 
spain_deaths = spain['deaths'] 

# #sweden
# mask_swe = covid['countriesAndTerritories'] == 'Sweden'
# sweden = covid.loc[mask_swe]
# sweden = sweden.set_index(['dateRep'])
# sweden_cases = sweden['cases'] 
# sweden_deaths = sweden['deaths'] 

# #switzerland
# mask_swi = covid['countriesAndTerritories'] == 'Switzerland'
# switzerland = covid.loc[mask_swi]
# switzerland = switzerland.set_index(['dateRep'])
# switzerland_cases = switzerland['cases'] 
# switzerland_deaths = switzerland['deaths'] 

# #United Kingdom
# mask_uk = covid['countriesAndTerritories'] == 'United_Kingdom'
# uk = covid.loc[mask_uk]
# uk = uk.set_index(['dateRep'])
# uk_cases = uk['cases'] 
# uk_deaths = uk['deaths'] 



# df_cases = pd.concat([austria_cases  , belgium_cases  , croatia_cases  , cyprus_cases  , czech_cases  ,
#              denmark_cases  , estonia_cases  , finland_cases  , france_cases  , germany_cases  , greece_cases  , 
#              hungary_cases  , iceland_cases  , ireland_cases  , italy_cases  , latvia_cases  , liechtenstein_cases  ,
#              lithuania_cases  , luxembourg_cases  , malta_cases  , netherlands_cases  , norway_cases  , poland_cases  ,
#              portugal_cases  , romania_cases  , slovakia_cases  , slovenia_cases  , spain_cases  , sweden_cases  , 
#              switzerland_cases  , uk_cases], axis = 1)


# df_deaths = pd.concat([austria_deaths  , belgium_deaths  , croatia_deaths  , cyprus_deaths  , czech_deaths  ,
#              denmark_deaths  , estonia_deaths  , finland_deaths  , france_deaths  , germany_deaths  , greece_deaths  , 
#              hungary_deaths  , iceland_deaths  , ireland_deaths  , italy_deaths  , latvia_deaths  , liechtenstein_deaths  ,
#              lithuania_deaths  , luxembourg_deaths  , malta_deaths  , netherlands_deaths  , norway_deaths  , poland_deaths  ,
#              portugal_deaths  , romania_deaths  , slovakia_deaths  , slovenia_deaths  , spain_deaths  , sweden_deaths  , 
#              switzerland_deaths  , uk_deaths], axis = 1)

df_cases = pd.concat([belgium_cases  , france_cases  , germany_cases , ireland_cases  , italy_cases , netherlands_cases , spain_cases], axis = 1)

df_deaths = pd.concat([belgium_deaths  , france_deaths  , germany_deaths , ireland_deaths  , italy_deaths , netherlands_deaths , spain_deaths], axis = 1)


df_cases['SUM_CASES'] = df_cases.sum(axis = 1)

df_cases = df_cases.sort_values(by = 'DATE')

df_deaths['SUM_DEATHS'] = df_deaths.sum(axis = 1)

df_cases['DATE'] = pd.to_datetime(df_cases.index, format = '%d/%m/%Y')

df_deaths['DATE'] = pd.to_datetime(df_deaths.index, format = '%d/%m/%Y')

# df_cases.to_csv('/Users/johannesthellmann/Desktop/europe_cases.csv', index = False)

# df_deaths.to_csv('/Users/johannesthellmann/Desktop/europe_deaths.csv', index = False)

#df_cases.to_csv('/Users/johannesthellmann/Desktop/eurostoxx_cases.csv', index = False)

#df_deaths.to_csv('/Users/johannesthellmann/Desktop/eurostoxx_deaths.csv', index = False)

