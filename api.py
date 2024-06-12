# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 06:48:46 2024

@author: luhud
"""
import requests

API_KEY = 'AIzaSyCRrUINAWYWUxu-qnkGKPRtNNWPdNGjmyw'
company_name = 'Concordia University'
url = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={company_name}&inputtype=textquery&fields=name,geometry&key={API_KEY}"

response = requests.get(url)
data = response.json()

if data['candidates']:
    location = data['candidates'][0]['geometry']['location']
    print(f"Location: {location}")
else:
    print("Company not found.")



url = f"https://nominatim.openstreetmap.org/search?q={company_name}&format=json"

response = requests.get(url)
data = response.json()

if data:
    location = data[0]['lat'], data[0]['lon']
    print(f"Location: {location}")
else:
    print("Company not found.")
    

import requests

API_KEY = 'YOUR_CLEARBIT_API_KEY'
company_name = 'Concordia University'
url = f"https://company.clearbit.com/v2/companies/find?name={company_name}"

headers = {
    'Authorization': f'Bearer {API_KEY}'
}

response = requests.get(url, headers=headers)
data = response.json()

if 'location' in data:
    location = data['location']
    print(f"Location: {location}")
else:
    print("Company not found.")
    
    
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 11:55:52 2024
"""

"""
Reference:
    https://github.com/googlemaps/google-maps-services-python
    https://developers.google.com/maps/documentation/geocoding/start
Google geocoding API

Install the following libraries:

pip install pandas
pip install googlemaps
pip install shapely
pip install collection
"""

import pandas as pd
import json
import googlemaps
from shapely.geometry import LineString, Point
from collections import Counter
import os
# Replace 'api_key' with your actual Google Maps API key
api_key = 'XXXXXXXXXXXXXXXXXXXXXXXX'
gmaps = googlemaps.Client(key=api_key)

def parse_geojson(data):
    try:
        geojson = json.loads(data)
        geometry_type = geojson.get("type")
        reversed_coordinates = None    
        if geometry_type == "LineString":
            coordinates = geojson.get("coordinates")
            reversed_coordinates = list(reversed(coordinates))     
        else:
            print(f"Unsupported geometry type: {geometry_type}")        
        return reversed_coordinates     
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None  
    
def extract_postcode(coord):
    try:
        reverse_geocode_result = gmaps.reverse_geocode((coord[1], coord[0]))     
        for result in reverse_geocode_result:
            for component in result['address_components']:
                if 'postal_code' in component.get('types', []):
                    if len(component.get('long_name', '')) == 7:  # Ensure postal code length is 7
                        return component['long_name']
        return None  # Return None if no valid postal code found
    except Exception as e:
        print("Error occurred:", e)
        return None
    
    

def get_list_postcodes(coords):
    postcodes = []  # array of postcodes
    for coord in coords:
        # Add a check for empty coordinates
        if None in coord:
            continue   
        try:
            #accept two arguements instead of a list
            postcode = extract_postcode(coord) 
            postcodes.append(postcode)
                
        except Exception as e:
            print(f"HTTP Error: {e}")

    print(postcodes)
    if not postcodes:
        print('NONE')
        return None   
    return postcodes

# From the list get most common postcodes
def get_most_common_element(input_list):
    # Filter out None values from input_list
    filtered_list = [x for x in input_list if x is not None]
    if filtered_list:  # Check if filtered_list is not empty
        counter = Counter(filtered_list)
        most_common_item = counter.most_common(1)
        return most_common_item[0][0]
    else:
        return None 

# Read the CSV file into a DataFrame
# Replace with the PATH of the file
filepath = 'XXXXXXXXXXXXXXXXXXXXXXXXXXX'
# Replace with the PATH of the new file saved
new_filepath = 'XXXXXXXXXXXXXXXXXXXXXXXXXXX'
pd.set_option('display.max_columns', 7)
pd.set_option('display.max_colwidth', 30)

df1 = pd.read_csv(filepath)
df1['POSTCODE'] = df1['POSTCODE'].astype(object)
df = df1[(df1['GEOM_GTYPE'] == 2) & (df1.index >= 0) & (df1.index < 100)]


# Create an empty list to store DataFrames
dfs = []

# Iterate through each row in the original DataFrame
for index, row in df.iterrows():
    try:
        geom_data = json.loads(row['GEOMETRY'])
    except (json.JSONDecodeError, TypeError) as e:
        print(f"Error decoding JSON at index {index}: {e}")
        continue
    
    geom_data = row['GEOMETRY']
    ID_PNO = [row['PNO']]
    ID_ENTRY = [row['ENTRY_ID']]
    coordinates = parse_geojson(geom_data)
    
    line_geometry = LineString(coordinates)
    POSTCODES = get_list_postcodes(line_geometry.coords)
    MOST_COMMON_POSTCODE = get_most_common_element(POSTCODES)
  
    df.loc[index, 'POSTCODE'] = MOST_COMMON_POSTCODE
    
    if coordinates:
            # Create a DataFrame for the coordinates
        coords_df = pd.DataFrame({'PNO': ID_PNO * len(coordinates),
                                      'ENTRY_ID': ID_ENTRY * len(coordinates),
                                      'GEOM_GTYPE': [None] * len(coordinates),
                                      'GEOMETRY': coordinates,
                                      'POSTCODE': POSTCODES})
        # Append the original row to dfs
        dfs.append(df.loc[[index]])
        # Append coords_df (new dataframe) to dfs
        dfs.append(coords_df)
           
    else:
            # If no coordinates, append only the original row
        dfs.append(pd.DataFrame([row]))

df2 = pd.concat(dfs, ignore_index=True)
df2.to_csv(new_filepath, index=False, mode='a', header=not os.path.exists(new_filepath))

print(df2)
print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
print("original df: \n", df)

