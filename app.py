import pandas as pd
import pgeocode
import geopy.distance
import math

nomi = pgeocode.Nominatim('us')
sandiego_nomi = nomi.query_location('San Diego')
san_diego_zips = [d.postal_code for index, d in sandiego_nomi.iterrows()]
sanjose_nomi = nomi.query_location('San Jose')
san_jose_zips = [d.postal_code for index, d in sanjose_nomi.iterrows()]



existing_craters = pd.read_csv('crater_data/existing_customers.csv')
existing_craters = existing_craters[existing_craters['County'] == 'CA']

new_craters = pd.read_csv('crater_data/new_craters.csv')
new_craters = new_craters[new_craters['State'] == 'CA']
new_craters = new_craters[new_craters['zip'].notnull()]

bill_craters = pd.read_csv('crater_data/bill_craters.csv')
bill_craters = bill_craters[bill_craters['State'] == 'CA']
bill_craters = bill_craters[bill_craters['zip'].notnull()]

sanDiego_latlng = [33.1101, -117.07]
sanJose_latlng = [37.2123, -121.7416]

san_diego_craters_data = {
    "name": [],
    "street_address": [],
    "city": [],
    "zip": [],
    "distance_from_san_diego": []
}


san_jose_craters_data = {
    "name": [],
    "street_address": [],
    "city": [],
    "zip": [],
    "distance_from_san_jose": []
}


        
def get_lat_long(zip):
    data = nomi.query_postal_code(zip)
    return [data.latitude, data.longitude]

def compare_dist_san_diego(latLong):
    for zip in san_diego_zips:
        lat_long = get_lat_long(zip)
        distance = geopy.distance.geodesic(latLong, lat_long).miles
        if distance <= 70:
            return distance
            break
    return False

def compare_dist_san_jose(latLong):
    for zip in san_jose_zips:
        lat_long = get_lat_long(zip)
        distance = geopy.distance.geodesic(latLong, lat_long).miles
        if distance <= 70:
            return distance
            break
    return False

  

def processDF(df):   
    for index, row in df.iterrows():
            if len(row['zip']) <= 5:
                lat_long = get_lat_long(row['zip'])
                dist_sandiego = compare_dist_san_diego(lat_long)
                dist_sanjose = compare_dist_san_jose(lat_long)
                if  dist_sandiego  != False:
                    san_diego_craters_data["name"].append(row['name'])
                    san_diego_craters_data['street_address'].append(row['address'])
                    san_diego_craters_data['city'].append(row['city'])
                    san_diego_craters_data['zip'].append(row['zip'])
                    san_diego_craters_data['distance_from_san_diego'].append(dist_sandiego)
                elif dist_sanjose != False:
                    san_jose_craters_data["name"].append(row['name'])
                    san_jose_craters_data['street_address'].append(row['address'])
                    san_jose_craters_data['city'].append(row['city'])
                    san_jose_craters_data['zip'].append(row['zip'])
                    san_jose_craters_data['distance_from_san_jose'].append(dist_sanjose)
            
            
processDF(new_craters)
processDF(bill_craters)
processDF(existing_craters)


craters_near_san_diego = pd.DataFrame(san_diego_craters_data)
craters_near_san_jose = pd.DataFrame(san_jose_craters_data)

craters_near_san_diego.to_csv('craters_near_san_diego.csv')
craters_near_san_jose.to_csv('craters_near_san_jose.csv')