# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 23:40:57 2016

@author: aditya
"""

import pandas as pd
import math

df = pd.read_csv("detroit-blight-violations.csv", low_memory=False)

#df.dropna(inplace=True)


df['lat1'] = df['ViolationAddress'].apply(
    lambda x: float(str(x).strip().split("(")[1].split(",")[0].strip()))
    
df['lon1'] = df['ViolationAddress'].apply(
    lambda x: float(str(x).strip().split("(")[1].split(",")[1].split(")")[0].strip()))

df['address'] = df['ViolationAddress'].apply(
    lambda x: str(x).split("(")[0].replace("\n",","))

df['lat'] = df['lat1'].apply(
    lambda x: math.ceil(x * 10000) / 10000)

df['lon'] = df['lon1'].apply(
    lambda x: math.ceil(x * 10000) / 10000)
    
df2 = df[['address', 'lat', 'lon', 'ViolDescription', 'PaymentStatus' ]].copy()
df = None

df2 = df2[ (df2.lon < -82.8774) & (df2.lon > -83.2880) ]
df2.reset_index(inplace=True)

df2 = df2[ (df2.lat > 42.2399) & (df2.lat < 42.4427) ]
df2.reset_index(inplace=True)

df3 = df2[['address', 'lat', 'lon', 'ViolDescription', 'PaymentStatus' ]].copy()
df3.to_csv("blight-location.csv", index=False)
df2 = None
    
