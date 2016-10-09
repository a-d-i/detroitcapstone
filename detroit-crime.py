# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 00:57:05 2016

@author: aditya
"""
import pandas as pd
import math

df = pd.read_csv("detroit-crime.csv", low_memory=False)
df = df[ (df.CATEGORY.str.contains("TRAFFIC") == False) &
           (df.CATEGORY.str.contains("TAX REVENUE") == False) &
           (df.CATEGORY.str.contains("MILITARY") == False)]
df2 = df[['ADDRESS', 'LAT', 'LON', 'CATEGORY', 'OFFENSEDESCRIPTION' ]].copy()
df2.dropna(inplace=True)
df2 = df2[ (df2.LON < -82.877426) & (df2.LON > -83.288055) ]
df2 = df2[ (df2.LAT > 42.239873) & (df2.LAT < 42.442725) ]
df = None

df3 = df2.copy()
df3['address'] = df2['ADDRESS']
df3['lat'] = df2['LAT'].apply(
    lambda x: math.ceil(float(str(x).split(",")[0])*10000)/10000)
df3['lon'] = df2['LON'].apply(
    lambda x: math.ceil(float(str(x).split(",")[0])*10000)/10000)
df2 = None    
df3.drop(['ADDRESS', 'LAT', 'LON'], axis=1, inplace=True)
df4 = df3[['address', 'lat', 'lon', 'CATEGORY', 'OFFENSEDESCRIPTION']]
df4.to_csv("crime_location_2.csv", index=False)


