# -*- coding: utf-8 -*-
"""
Created on Sat Jul  9 23:59:24 2016

@author: aditya
"""
import pandas as pd
import math
#import numpy  as np

building_id = 0
buildings = {}

def get_building_id():
    global building_id
    building_id += 1
    return building_id

df  = pd.read_csv("detroit-311.csv")
df2 = df[['address', 'location', 'issue_description']]
df = None
df2.dropna(inplace=True)
df2.location = df2['location'].apply(
    lambda x: str(x).strip().replace("(","").replace(")",""))

df2['lat'] = df2['location'].apply(
    lambda x: math.ceil(float(str(x).split(",")[0])*10000)/10000)
    
df2['lon'] = df2['location'].apply(
    lambda x: math.ceil(float(str(x).split(",")[1])*10000)/10000)

df2 = df2[ (df2.lon < -82.8774) & (df2.lon > -83.2880) ]
df2 = df2[ (df2.lat > 42.2399) & (df2.lat < 42.4427) ]
df2.reset_index(inplace=True,drop=True)

df2.drop(['location'], axis=1, inplace=True)    
df3 = df2[['address','lat','lon','issue_description']]
df3.to_csv("311location_2.csv", index=False)
#df2 = None

L = len(df2.lat)

for i in xrange(L):
    lat = round(df2.lat[i],4)
    lon = round(df2.lon[i],4)
    if buildings.has_key(lat):
        if buildings[lat].has_key(lon):
            buildings[lat][lon].append(df2.address[i])
        else:
            buildings[lat][lon] = [get_building_id(), df2.address[i]]
    else:
        myLon = {}
        myLon[lon] = [get_building_id(), df2.address[i]]
        buildings[lat] = myLon

building_id        
i = None
lat = None
lon = None
myLon = None
L = None
        


