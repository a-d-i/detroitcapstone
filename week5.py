# -*- coding: utf-8 -*-
"""
@author: aditya
"""
from __future__ import print_function
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.cross_validation import  cross_val_score

###########################################################################
# categorical to numerical dictionaries
###########################################################################
issue_to_int = {
  ".*vacant.*"  :1.0, 
  ".*empty.*"   :1.0, 
  ".*blight.*"  :1.0, 
  ".*weeds.*"   :1.0, 
  ".*debris.*"  :1.0, 
  ".*grass.*"   :1.0, 
  ".*garbage.*" :1.0, 
  ".*trash.*"   :1.0,
  ".*VACANT.*"  :1.0, 
  ".*EMPTY.*"   :1.0, 
  ".*BLIGHT.*"  :1.0, 
  ".*WEEDS.*"   :1.0, 
  ".*DEBRIS.*"  :1.0, 
  ".*GRASS.*"   :1.0, 
  ".*GARBAGE.*" :1.0, 
  ".*TRASH.*"   :1.0,
  ".*drain.*"  :0.5, 
  ".*sink.*"   :0.5, 
  ".*clogged.*"  :0.5, 
  ".*flooding.*"   :0.5, 
  ".*DRAIN.*"  :0.5, 
  ".*SINK.*"   :0.5, 
  ".*CLOGGED.*"  :0.5, 
  ".*FLOODING.*"   :0.5
}

violdesc_to_int = {
  ".*48 hours.*"  :1.0,
  ".*48 HOURS.*"  :1.0,
  ".*waste.*"  :1.0,
  ".*WASTE.*"  :1.0
}

payment_to_int = {
  "PAID IN FULL": -1.0,
  "NO PAYMENT APPLIED" : 0.5,
  "PARTIAL PAYMENT MADE": 0.5,
  "NO PAYMENT ON RECORD" : 1.0
}

category_to_int = {
  ".*HEALTH-SAFETY.*"  :1.0,
  ".*VAGRANCY.*"  :1.0,
  ".*ENVIRONMENT.*"  :1.0,
  ".*DAMAGE TO PROPERTY.*"  :1.0,
  ".*stolen vehicle.*"  :0.0,
  ".*traffic.*"  :0.0,
  ".*JUDICIARY.*"  :0.0,
  ".*VEHICLE.*"  :0.0,
  ".*KIDNAPING.*"  :0.0,
  ".*BRIBERY.*"  :0.0,
  ".*STOLEN.*"  :0.0,
  ".*OBSTRUCTING.*"  :0.0,
  ".*FORGERY.*"  :0.0,
  ".*SOVEREIGNTY.*"  :0.0,
  ".*ANTITRUST.*"  :0.0,
  ".*FORGERY.*"  :0.0,
  ".*HOMICIDE.*"  :0.0
}

offdesc_to_int = {
  ".*destroying.*"  :1.0,
  ".*DESTROYING.*"  :1.0,
  ".*property.*"  :1.0,
  ".*PROPERTY.*"  :1.0,
  ".*arson.*"  :0.5,
  ".*ARSON.*"  :0.5,
  ".*transport.*"  :0.5,
  ".*TRANSPORT.*"  :0.5,
  ".*traffic.*"  :0.5,
  ".*TRAFFIC.*"  :0.5,
  ".*accidents.*"  :0.5,
  ".*ACCIDENTS.*"  :0.5,
  ".*BAC.*"  :0.5
}

###########################################################################
# building counter
###########################################################################
bldg_cntr = {}

def bldgcounter(x):
  global bldg_cntr
  bldgid = int(x[0])
  try:      
      v = bldg_cntr[bldgid]
      v = v + 1
      bldg_cntr[bldgid] = v
  except:
      bldg_cntr[bldgid] = 1
  return


###########################################################################
# building data structure
###########################################################################
building_id = 1
buildings = {}
label = {}

###########################################################################
# generating unique building ids 
###########################################################################
def get_building_id():
    global building_id
    building_id += 1
    label[building_id] = 0
    return building_id

###########################################################################
# demo buildings 
###########################################################################
df_demo = pd.read_csv("demo-permit-location.csv")

###########################################################################
# concatenate cleaned data from all 3 non demolition files 
###########################################################################
df_311   = pd.read_csv("311location_2.csv")
df_bl    = pd.read_csv("blight-location.csv")
df_crime = pd.read_csv("crime_location_2.csv")

frames = [df_311, df_crime, df_bl] 
df = pd.concat(frames, ignore_index=True, axis=0)

df2 = df[['address', 'lat', 'lon', 'CATEGORY', 'OFFENSEDESCRIPTION', 'PaymentStatus', 'ViolDescription', 'issue_description']].copy()
df     = df2
df2    = None
frames = None

###########################################################################
# generate list of buildings
###########################################################################
L = len(df.lat)

for i in xrange(L):
    lat = round(df.lat[i],4)
    lon = round(df.lon[i],4)
    if buildings.has_key(lat):
        if buildings[lat].has_key(lon):
            buildings[lat][lon].append(df.address[i])
        else:
            buildings[lat][lon] = [get_building_id(), df.address[i]]
    else:
        myLon = {}
        myLon[lon] = [get_building_id(), df.address[i]]
        buildings[lat] = myLon

###########################################################################
# cleaup varilables not needed anymore
###########################################################################
i        = None
lat      = None
lon      = None
myLon    = None
L        = None
df_311   = None
df_bl    = None
df_crime = None

###########################################################################
# add building id to data
###########################################################################
def addbldgid(x):
  global buildings
  try:
    lat = round(x[1],4)
    lon = round(x[2],4)
    v = buildings[lat][lon]
    v_id = v[0]
    return v_id
  except:
    return 0

###########################################################################
#  add building id to non-demo and demo data
###########################################################################
# by default put unknown building_id (value 0)
df['building_id'] = df.apply(addbldgid, axis=1)
df_demo['building_id'] = df_demo.apply(addbldgid, axis=1)
df_demo = df_demo[ df_demo.building_id != 0]

###########################################################################
#  df processing
###########################################################################
df.issue_description.fillna(-1.0, inplace=True)
df['issueint'] = df.issue_description.replace(issue_to_int, regex=True)
df['issueint'] = df['issueint'].convert_objects(convert_numeric=True)
df['issueint']  = df['issueint'].replace('nan', 0.0)

df.ViolDescription.fillna(-1.0, inplace=True)
df['violint']  = df.ViolDescription.replace(violdesc_to_int, regex=True)
df['violint']  = df['violint'].convert_objects(convert_numeric=True)
df['violint']  = df['violint'].replace('nan', 0.0)

df.PaymentStatus.fillna(-1.0, inplace=True)
df['paymentint']  = df.PaymentStatus.replace(payment_to_int, regex=True)
df['paymentint']  = df['paymentint'].convert_objects(convert_numeric=True)
df['paymentint']  = df['paymentint'].replace('nan', 0.0)

df.CATEGORY.fillna(-1.0, inplace=True)
df['categoryint']  = df.CATEGORY.replace(category_to_int, regex=True)
df['categoryint']  = df['categoryint'].convert_objects(convert_numeric=True)
df['categoryint']  = df['categoryint'].replace('nan', 0.0)

df.OFFENSEDESCRIPTION.fillna(-1.0, inplace=True)
df['offenseint']  = df.CATEGORY.replace(offdesc_to_int, regex=True)
df['offenseint']  = df['offenseint'].convert_objects(convert_numeric=True)
df['offenseint']  = df['offenseint'].replace('nan', 0.0)

del df['CATEGORY']
del df['PaymentStatus']
del df['OFFENSEDESCRIPTION']
del df['ViolDescription']
del df['issue_description']
del df['lat']
del df['lon']
del df['address']

df = df[['building_id', 'issueint', 'violint', 'paymentint', 'categoryint', 'offenseint']]
df.apply(bldgcounter, axis=1)

del df_demo['lat']
del df_demo['lon']
del df_demo['address']

df_demo.apply(bldgcounter, axis=1)

df_dfcounter = pd.DataFrame.from_dict(bldg_cntr, orient='index')
df_dfcounter.columns = ['count']
df_dfcounter['building_id'] = df_dfcounter.index
df_dfcounter = df_dfcounter[['building_id', 'count']]

dfn = df.groupby('building_id', as_index=False).sum()
df = None
df = dfn[['building_id', 'issueint', 'violint', 'paymentint', 'categoryint', 'offenseint']]
dfn = None
df.reset_index(inplace=True, drop=True)

df = df.merge(df_dfcounter, on='building_id')
df.reset_index(inplace=True, drop=True)
df_dfcounter = None

###########################################################################
# blighted buildings labelling data - df_demo
###########################################################################
targetbldg = df_demo.building_id.unique()
tlist = list(targetbldg)

df_demo = None
df_demo = pd.DataFrame(targetbldg)
df_demo.columns = ['building_id']
df_demo['target'] = 1
#
df_final = df.merge(df_demo, on='building_id')

df_target0 = df[~df.building_id.isin(tlist)].copy()
df_target0['target'] = 0
df_target00 = df_target0.iloc[np.random.permutation(len(df_target0))]

df_target0 = None
df_target0 = df_target00[0:len(df_final)+5000]

df_result1 = pd.concat([df_final, df_target0], axis=0)
df_result = df_result1.iloc[np.random.permutation(len(df_result1))]
df_result.reset_index(inplace=True, drop=True)
df_result1  = None
df_target0  = None
df_target00 = None

df_result.to_csv("week5_data.csv", index=False)


###########################################################################
# processing to create labelled data
###########################################################################
y = df_result['target']
features = list(df_result.columns[1:7])
X = df_result[features]

dt = DecisionTreeClassifier(min_samples_split=20, random_state=99)

dt.fit(X, y)

scores = cross_val_score(dt, X, y, cv=5)

print("mean: {:.3f} (std: {:.3f})".format(scores.mean(),scores.std()), end="\n\n")

