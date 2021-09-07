from inspect import classify_class_attrs
from urllib.parse import DefragResult
import pandas as pd
from geopy.geocoders import GoogleV3
import geopy.distance
import googlemaps
import itertools    

API=''
geolocator = GoogleV3(api_key=API)
gmaps = googlemaps.Client(key=API)
df = pd.read_csv('Direct to Store list_v1.csv')
df = df.iloc[:-6630]
og = df['Address 1'].astype(str)
dest = df['MAILING ADDRESS'].astype(str)

df['ocode'] = og.apply(geolocator.geocode)
df['OLat'] = [g.latitude for g in df.ocode]
df['OLong'] = [g.longitude for g in df.ocode]
df['OCoord'] = df['OLat'].astype(str) + ',' + df['OLong'].astype(str)

df['dcode'] = dest.apply(geolocator.geocode)
df['DLat'] = [g.latitude for g in df.dcode]
df['DLong'] = [g.longitude for g in df.dcode]
df['DCoord'] = df['DLat'].astype(str) + ',' + df['DLong'].astype(str)

durList = []
actual_duration = []

distList = []
actual_distance = []

result = gmaps.distance_matrix(df['OCoord'], df['DCoord'], mode='driving')['rows'][0]
# print(result)
for elements in result['elements']:
    dur = elements.get('duration').get('value')
    dist = elements.get('distance').get('value')

    durList.append(dur)
    distList.append(dist)

    dur = dur/3600
    dist = dist/1000

    actual_duration.append(dur)
    actual_distance.append(dist)

df['Duration (Hours)'] = actual_duration
df['Distance (KM)'] = actual_distance

df = df[['Vendor#', 'Province / State', 'Address 1', 'Postal / Zip Code', 'Direct to store Dest', 'Province', 'OLat', 'OLong', 'OCoord', 'MAILING ADDRESS', 'Postal', 'DLat', 'DLong', 'DCoord', 'Copy & Paste the link in browser', 'ocode', 'dcode', 'Duration (Hours)', 'Distance (KM)']]
print(df)