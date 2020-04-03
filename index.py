# /index.py
import datetime
from flask import Flask, request, jsonify, render_template
import os
import dialogflow
import requests
import json
import pusher
import sys
sys.path.insert(0,'./Source/tagui-v1.1/')
import rpa_main as airbnb
from pandas.io.json import json_normalize
import pandas as pd
import folium
from geopy.geocoders import Nominatim 

app = Flask(__name__)
CLIENT_ID = 'NFTR233O0S1IITFK10EHZURRRQOB4UAPI1RYXSKE4HAY4UNU'
CLIENT_SECRET = 'ECNBJE3PPFMAMT2US14SIWOKNA15FSK03O321JMNZYWFT4PY'

@app.route('/get_recommendations', methods=['POST'])
def index():
    data = request.get_json(silent=True)

    country = data['queryResult']['parameters']['city']
    numOfAdults = data['queryResult']['parameters']['numOfAdults']
    numOfInfants = data['queryResult']['parameters']['numOfInfants']
    numOfChildren = data['queryResult']['parameters']['numOfChildren']
    fromDate = data['queryResult']['parameters']['fromDate']
    toDate = data['queryResult']['parameters']['toDate']

    print("Country: "+str(country) +",\n"
            +"Number of People: "+str(numOfAdults)+",\n"
            +"From: "+str(fromDate)+",\n"
            +"To: "+str(toDate)+".\n")

    fromDate = formatDate(fromDate)
    toDate = formatDate(toDate)
    get_venues('test')
    #response = airbnb.process(country, int(numOfAdults), int(numOfInfants), int(numOfChildren), fromDate, toDate)
    response="HIHIHI"
    reply = {
            "fulfillmentText": response,
        }
    return jsonify(reply)

def formatDate(date):
    formattedDate = date
    formattedDate = formattedDate.split("T")[0]    
    formattedDate = formattedDate.split("-")
    formattedDate = datetime.datetime(int(formattedDate[0]), int(formattedDate[1]), int(formattedDate[2]))
    formattedDate = formattedDate.strftime('X%d').replace('X0', '').replace('X','') +" "+ formattedDate.strftime('%B') +" "+ formattedDate.strftime('%Y')

    return formattedDate

def get_venues(listings):
    url = 'https://api.foursquare.com/v2/venues/explore'

    params = dict(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    v='20200401',
    ll='1.323681 ,103.947566',
    limit=10,
    radius = 600
    )
    resp = requests.get(url=url, params=params).json()
    
    venues = resp['response']['groups'][0]['items']
    #nearby_venues = json_normalize(venues)
    #columns = ['venue.name', 'venue.categories.[0].name', 'venue.location.lat', 'venue.location.lng']
    nearby_venues = pd.DataFrame(columns=['Name', 'Category', 'Latitude', 'Longitude'])
    for venue in venues:
        df = pd.DataFrame([(venue['venue']['name'], 
                            venue['venue']['categories'][0]['name'],
                            venue['venue']['location']['lat'], 
                            venue['venue']['location']['lng'])], columns=['Name', 'Category', 'Latitude', 'Longitude'])
        nearby_venues = nearby_venues.append(df, ignore_index=True)
    print(nearby_venues.head())
    #map = folium.Map([51., 12.], zoom_start=6,control_scale=True)
    #folium.GeoJson(data).add_to(map)
    #map.save('map.html')
    
    return ""

# run Flask app
if __name__ == "__main__":
    app.run()