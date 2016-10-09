# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 00:53:10 2016

@author: aditya
"""

import pandas as pd
import math

def fnlat(x):
    try:
      k = x.strip().split("(")[1]
      if k:
        return x.strip().split("(")[1].split(",")[0].strip()
      else:
        return "-9999"
    except:
        return "-9999"

def fnlon(x):
    try:
      k = x.strip().split("(")[1]
      if k:
        return x.strip().split("(")[1].split(",")[1].split(")")[0].strip()
      else:
        return "-9999"
    except:
        return "-9999"

df2 = pd.read_table("detroit-demolition-permits.tsv", low_memory=False)
df = df2[['SITE_ADDRESS', 'site_location']]
df2 = None

df['lat1'] = df['site_location'].apply(
    lambda x: float(fnlat(x)))
    
df['lon1'] = df['site_location'].apply(
    lambda x: float(fnlon(x)))
    
df['lat'] = df['lat1'].apply(
    lambda x: math.ceil(x * 10000) / 10000)
    
df['lon'] = df['lon1'].apply(
    lambda x: math.ceil(x * 10000) / 10000)
    
df['address'] = df['SITE_ADDRESS']

df = df[ (df.lon < -82.8774) & (df.lon > -83.2880) ]
df.reset_index(inplace=True)
df = df[ (df.lat > 42.2399) & (df.lat < 42.4427) ]
df.reset_index(inplace=True)
    
df2 = df[['address', 'lat', 'lon']].copy()
df2.to_csv("demo-permit-location.csv", index=False)
df = None
