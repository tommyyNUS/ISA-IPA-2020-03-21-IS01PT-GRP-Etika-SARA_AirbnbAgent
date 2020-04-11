# /index.py
import datetime
from datetime import date
from flask import Flask, request, jsonify, render_template
import os
import dialogflow
import requests
import json
import pusher
import sys
sys.path.insert(0,'./Source/tagui-v1.2/')
import rpa_main as airbnb
from pandas.io.json import json_normalize
import pandas as pd
import folium
from geopy.geocoders import Nominatim
import pyshorteners
import telegram
from folium.features import DivIcon
import time
import rpa as r
from branca.element import Template, MacroElement

app = Flask(__name__)
CLIENT_ID = 'NFTR233O0S1IITFK10EHZURRRQOB4UAPI1RYXSKE4HAY4UNU'
CLIENT_SECRET = 'ECNBJE3PPFMAMT2US14SIWOKNA15FSK03O321JMNZYWFT4PY'
bot_token = '1080638501:AAHhksiyyTfavxdcr8SXPZWFQpmV2Hx2mK0'
bot = telegram.Bot(token=bot_token)

@app.route('/get_html')
def get_html():
    return render_template('./map.html')

@app.route('/get_recommendations', methods=['POST'])
def index():
    data = request.get_json(silent=True)
    print("--- Data ---")
    print(data)
    
    #Check if telegram bot
    telegramChannel = False
    telegramChatID = ""
    if 'source' in data['originalDetectIntentRequest'] and data['originalDetectIntentRequest']['source'] == 'telegram':
        telegramChatID = data['originalDetectIntentRequest']['payload']['data']['from']['id']
        telegramChannel = True
    
    country = data['queryResult']['parameters']['city']
    numOfAdults = data['queryResult']['parameters']['numOfAdults']
    numOfInfants = data['queryResult']['parameters']['numOfInfants']
    numOfChildren = data['queryResult']['parameters']['numOfChildren']
    fromDate = data['queryResult']['parameters']['fromDate']
    toDate = data['queryResult']['parameters']['toDate']
    durationOfStay = getDurationOfStay(data['queryResult']['parameters']['fromDate'], data['queryResult']['parameters']['toDate'])
    print("Country: "+str(country) +",\n"
            +"Number of People: "+str(numOfAdults)+",\n"
            +"From: "+str(fromDate)+",\n"
            +"To: "+str(toDate)+".\n")

    fromDate = formatDate(fromDate)
    toDate = formatDate(toDate)
    
    #response = airbnb.process(country, int(numOfAdults), int(numOfInfants), int(numOfChildren), fromDate, toDate)
    response = {'0': {'name': 'Exklusive 2 Zimmer Wohnung am grünen Prater 13/62', 'description': 'Vienna', 'inventory': '4 guests 1 bedroom 2 beds 1 bathroom', 'price': '$498', 'rating': 'Rating 4.80 out of 5 (83 reviews)', 'picurl': ['https://a0.muscache.com/im/pictures/pro_photo_tool/Hosting-24419779-unapproved/original/2883724e-06bc-4892-bbfb-88941a62d4e2.JPEG?aki_policy=xx_large', 'https://a0.muscache.com/im/pictures/pro_photo_tool/Hosting-24419779-unapproved/original/dd318a5c-750b-464b-8123-c01af1322a8c.JPEG?aki_policy=xx_large', 'https://a0.muscache.com/im/pictures/pro_photo_tool/Hosting-24419779-unapproved/original/e8d2a7c4-a144-4c79-a893-fb80f42fbf16.JPEG?aki_policy=xx_large', 'https://a0.muscache.com/im/pictures/pro_photo_tool/Hosting-24419779-unapproved/original/ffd47e34-835f-4c43-b419-52068b7130cd.JPEG?aki_policy=xx_large', 'https://a0.muscache.com/im/pictures/pro_photo_tool/Hosting-24419779-unapproved/original/add40cd9-b79d-43d1-8f24-d4b97fd77287.JPEG?aki_policy=xx_large', 'https://a0.muscache.com/im/pictures/pro_photo_tool/Hosting-24419779-unapproved/original/d7722077-0973-443b-b1a6-aa4a7b1f4b20.JPEG?aki_policy=xx_large', 'https://a0.muscache.com/im/pictures/pro_photo_tool/Hosting-24419779-unapproved/original/f013481c-3d85-49cf-b4b2-f996a10bc7c5.JPEG?aki_policy=xx_large', 'https://a0.muscache.com/im/pictures/pro_photo_tool/Hosting-24419779-unapproved/original/3f1c8d43-c48f-4a4a-98f5-cd9ff5599d9c.JPEG?aki_policy=xx_large', 'https://a0.muscache.com/im/pictures/pro_photo_tool/Hosting-24419779-unapproved/original/b4d0fcc1-b62f-4a4a-a2d2-c2a4f837e2c1.JPEG?aki_policy=xx_large', 'https://a0.muscache.com/im/pictures/pro_photo_tool/Hosting-24419779-unapproved/original/64caaf27-b9d4-4fc9-9315-64a6638af7b1.JPEG?aki_policy=xx_large'], 'pictext': ['Exklusive 2 Zimmer Wohnung am grünen Prater 13/62', 'Exklusive 2 Zimmer Wohnung am grünen Prater 13/62', 'Exklusive 2 Zimmer Wohnung am grünen Prater 13/62', 'Exklusive 2 Zimmer Wohnung am grünen Prater 13/62', 'Exklusive 2 Zimmer Wohnung am grünen Prater 13/62', 'Exklusive 2 Zimmer Wohnung am grünen Prater 13/62', 'Exklusive 2 Zimmer Wohnung am grünen Prater 13/62', 'Exklusive 2 Zimmer Wohnung am grünen Prater 13/62', 'Exklusive 2 Zimmer Wohnung am grünen Prater 13/62', 'Exklusive 2 Zimmer Wohnung am grünen Prater 13/62'], 'url': 'https://www.airbnb.com.sg/rooms/24419779?location=Vienna&adults=1&children=1&infants=1&check_in=2020-06-05&check_out=2020-06-17&previous_page_section_name=1000&federated_search_id=f2b26c9a-0037-4870-88ee-5ab956cd130e', 'coordinates': '48.21139,16.41125'}, '1': {'name': '90sqm - Terrace - Near Danube - AC +  Netflix', 'description': 'Vienna', 'inventory': '6 guests 2 bedrooms 3 beds 1.5 bathrooms', 'price': '$1,534', 'rating': 'Rating 4.96 out of 5 (27 reviews)', 'picurl': ['https://a0.muscache.com/im/pictures/8a2725d2-271d-42e8-afb6-d8ba338ebab5.jpg?aki_policy=xx_large', 'https://a0.muscache.com/im/pictures/47b222db-90c3-4061-8b28-a35f575ba6c9.jpg?aki_policy=xx_large', 'https://a0.muscache.com/im/pictures/47cb6595-3fa1-4e80-bca4-463cdf56c70c.jpg?aki_policy=xx_large', 'https://a0.muscache.com/im/pictures/82851dfb-24d1-4bd0-962d-295de2b894c1.jpg?aki_policy=xx_large', 'https://a0.muscache.com/im/pictures/4be9101e-20b3-4c49-b9a4-e7d50ba6d2cc.jpg?aki_policy=xx_large', 'https://a0.muscache.com/im/pictures/d93b81fb-b7c6-4d3e-a1e0-077d961bddcd.jpg?aki_policy=xx_large', 'https://a0.muscache.com/im/pictures/85f408ba-93c9-4252-bc90-b8422c30a643.jpg?aki_policy=xx_large', 'https://a0.muscache.com/im/pictures/2114a763-5254-4f17-ba74-84caafde6e49.jpg?aki_policy=xx_large', 'https://a0.muscache.com/im/pictures/21c9a91f-7140-4ad5-8858-1101787b70f2.jpg?aki_policy=xx_large', 'https://a0.muscache.com/im/pictures/d5f26e43-859c-46fe-a86e-810ec5f29e72.jpg?aki_policy=xx_large'], 'pictext': ['Living room with kitchenette', 'Living room with kitchenette', 'Living room with kitchenette', '15sqm terrace with outdoor shower', '15sqm terrace with outdoor shower', '15sqm terrace with outdoor shower', 'Bedroom 1 with 160cm wide double bed', 'Bedroom 1 with 160cm wide double bed', 'Bedroom 2 with 180cm wide double bed', 'Bedroom 2 with 180cm wide double bed'], 'url': 'https://www.airbnb.com.sg/rooms/38382634?location=Vienna&adults=1&children=1&infants=1&check_in=2020-06-05&check_out=2020-06-17&previous_page_section_name=1000&federated_search_id=f2b26c9a-0037-4870-88ee-5ab956cd130e', 'coordinates': '48.224,16.407'}, '2': {'name': 'Für Köche und Familien: Appartment mit Herz', 'description': 'Vienna', 'inventory': '4 guests 2 bedrooms 2 beds 1.5 bathrooms', 'price': '$790', 'rating': 'Rating 4.85 out of 5 (71 reviews)', 'picurl': ['https://a0.muscache.com/im/pictures/75b9e456-8589-4795-a259-fc5c48a57113.jpg?aki_policy=xx_large', 'https://a0.muscache.com/im/pictures/2f24dd61-1756-4394-9fe1-f2f77560fc42.jpg?aki_policy=xx_large', 'https://a0.muscache.com/im/pictures/f44840f1-035e-47a0-8ac8-c00308efa09b.jpg?aki_policy=xx_large', 'https://a0.muscache.com/im/pictures/ac050323-e3ca-4e8a-85ed-fcd9cdb19d8b.jpg?aki_policy=xx_large', 'https://a0.muscache.com/im/pictures/e0037ace-e6cb-4ac6-bdcb-9cadbb6cfbab.jpg?aki_policy=xx_large', 'https://a0.muscache.com/im/pictures/98f6fb19-eae4-4580-bb49-742d6d5f3148.jpg?aki_policy=xx_large', 'https://a0.muscache.com/im/pictures/09d9d2ae-738b-4150-853d-4a3b7a6551ce.jpg?aki_policy=xx_large', 'https://a0.muscache.com/im/pictures/85501a97-8f2a-4521-b70a-ecb02dcb0bee.jpg?aki_policy=xx_large', 'https://a0.muscache.com/im/pictures/c6acf8b4-f550-4368-8824-9459b89ccc2b.jpg?aki_policy=xx_large', 'https://a0.muscache.com/im/pictures/592adae0-289d-404c-ba3c-66fa3f2c46cb.jpg?aki_policy=xx_large'], 'pictext': ['Wohn-/Schlafraum, Queensize-Bett, TV;', 'Für Köche und Familien: Appartment mit Herz', 'Für Köche und Familien: Appartment mit Herz', 'Schlafzimmer Kingsize mit Tempur Luxusmatratzen', 'Für Köche und Familien: Appartment mit Herz', 'Für Köche und Familien: Appartment mit Herz', 'Für Köche und Familien: Appartment mit Herz', 'Für Köche und Familien: Appartment mit Herz', 'Für Köche und Familien: Appartment mit Herz', 'Favoritenstraße vom Reumannplatz Richtung Kalenberg, links Ameling-Haus'], 'url': 'https://www.airbnb.com.sg/rooms/22465162?location=Vienna&adults=1&children=1&infants=1&check_in=2020-06-05&check_out=2020-06-17&previous_page_section_name=1000&federated_search_id=f2b26c9a-0037-4870-88ee-5ab956cd130e', 'coordinates': '48.174,16.38'}, '3': {'name': "GOODMAN'S HOME VIENNA VI", 'description': 'Vienna', 'inventory': '4 guests 1 bedroom 2 beds 1 bathroom', 'price': '$573', 'rating': 'Rating 4.67 out of 5 (72 reviews)', 'picurl': ['https://a0.muscache.com/im/pictures/32cb74dc-28fe-463c-b66b-f2e11e587848.jpg?aki_policy=xx_large', 'https://a0.muscache.com/im/pictures/9739cfbe-a0bf-4551-9c13-70a0012868a0.jpg?aki_policy=xx_large', 'https://a0.muscache.com/im/pictures/831b9c1e-2580-49d2-b320-accf6ba30dbd.jpg?aki_policy=xx_large', 'https://a0.muscache.com/im/pictures/5d93086e-4dd5-4a56-88d1-ca031f4f375b.jpg?aki_policy=xx_large', 'https://a0.muscache.com/im/pictures/5ad437c6-4f43-46ba-b0f4-30c42eced0e5.jpg?aki_policy=xx_large', 'https://a0.muscache.com/im/pictures/17f1798a-2174-4d7c-87c4-4bbd24e7aa11.jpg?aki_policy=xx_large', 'https://a0.muscache.com/im/pictures/81c70780-b0d2-46ba-aa1d-cea50b0c48bb.jpg?aki_policy=xx_large', 'https://a0.muscache.com/im/pictures/80818062-4f03-4a11-9532-2a06d8d0f2b2.jpg?aki_policy=xx_large', 'https://a0.muscache.com/im/pictures/d648fb53-f657-42ef-bb23-7c4889f8a423.jpg?aki_policy=xx_large', 'https://a0.muscache.com/im/pictures/0f697119-d22c-4acf-b2af-8b0dea337b00.jpg?aki_policy=xx_large'], 'pictext': ["GOODMAN'S HOME VIENNA VI", "GOODMAN'S HOME VIENNA VI", "GOODMAN'S HOME VIENNA VI", "GOODMAN'S HOME VIENNA VI", "GOODMAN'S HOME VIENNA VI", 'Vintage chair from the 50s', "GOODMAN'S HOME VIENNA VI", "GOODMAN'S HOME VIENNA VI", "GOODMAN'S HOME VIENNA VI", "GOODMAN'S HOME VIENNA VI"], 'url': 'https://www.airbnb.com.sg/rooms/32583345?location=Vienna&adults=1&children=1&infants=1&check_in=2020-06-05&check_out=2020-06-17&previous_page_section_name=1000&federated_search_id=f2b26c9a-0037-4870-88ee-5ab956cd130e', 'coordinates': '48.22042,16.33047'}, '4': {'name': 'Helle Altbauwohnung 54m²- Bright 2 Room Apartment', 'description': 'Vienna', 'inventory': '6 guests 1 bedroom 2 beds 1 bathroom', 'price': '$1,871', 'rating': 'Rating 4.77 out of 5 (44 reviews)', 'picurl': ['https://a0.muscache.com/im/pictures/1b0e1fd1-4f4c-4503-b54e-15bd1ffe4a09.jpg?aki_policy=xx_large', 'https://a0.muscache.com/im/pictures/d962a9b3-6e10-4668-9bd4-1f95766feddb.jpg?aki_policy=xx_large', 'https://a0.muscache.com/im/pictures/119a5e8b-08f4-4c2d-a411-953da1eaf45e.jpg?aki_policy=xx_large', 'https://a0.muscache.com/im/pictures/ffff7b3d-e80f-4467-9595-0b92fcc2de13.jpg?aki_policy=xx_large', 'https://a0.muscache.com/im/pictures/1b6d22e0-0c9e-4466-ab6f-a6331a9f6672.jpg?aki_policy=xx_large', 'https://a0.muscache.com/im/pictures/400d9422-c6af-42d0-8efb-4c48c3829940.jpg?aki_policy=xx_large', 'https://a0.muscache.com/im/pictures/eaf40577-d924-41a5-a04b-988e154c2d8c.jpg?aki_policy=xx_large', 'https://a0.muscache.com/im/pictures/1b0e1fd1-4f4c-4503-b54e-15bd1ffe4a09.jpg?aki_policy=xx_large', 'https://a0.muscache.com/im/pictures/d962a9b3-6e10-4668-9bd4-1f95766feddb.jpg?aki_policy=xx_large', 'https://a0.muscache.com/im/pictures/119a5e8b-08f4-4c2d-a411-953da1eaf45e.jpg?aki_policy=xx_large'], 'pictext': ['Spacious living room area with a comfortable couch and soft bed.', 'Bedroom with double bed and double bunk bed on top. Comfortable cushions and blankets.', 'Well-equipped kitchen with all amenities. Stove, oven, fridge etc.', 'Living room. Perfect place to enjoy a home cooked meal at the dining room table.', 'Clean bathroom.', 'Single shower.', 'Our flower apartment welcoming you to Vienna!', 'Spacious living room area with a comfortable couch and soft bed.', 'Bedroom with double bed and double bunk bed on top. Comfortable cushions and blankets.', 'Well-equipped kitchen with all amenities. Stove, oven, fridge etc.'], 'url': 'https://www.airbnb.com.sg/rooms/20432408?location=Vienna&adults=1&children=1&infants=1&check_in=2020-06-05&check_out=2020-06-17&previous_page_section_name=1000&federated_search_id=f2b26c9a-0037-4870-88ee-5ab956cd130e', 'coordinates': '48.226,16.35'}}
    process_reponse(response, country, numOfAdults, numOfInfants, numOfChildren, fromDate, toDate, durationOfStay, telegramChatID, telegramChannel)

    #Dialogflow will timeout after 5 seconds, this reply is given in case RPA fails 
    reply = {
        "fulfillmentText" : "We are processing your request, this will take a few minutes."
    }
    return jsonify(reply)

def process_reponse(response, country, numOfAdults, numOfInfants, numOfChildren, fromDate, toDate, durationOfStay, telegramChatID, telegramChannel):
    stringResponse = "<u><b>Your search criteria</b></u>\n" + "City: "+country+"\nAdults: "+str(int(numOfAdults))+"\nInfants: "+str(int(numOfInfants))+"\nChildren: "+str(int(numOfChildren))+"\nFrom: "+fromDate+"\nTo: "+toDate+"\nDuration of stay(days): "+str(durationOfStay)+"\n\n"
    stringResponse = stringResponse + "Here are your 5 most recommended listings...\n"
    i=1
    s = pyshorteners.Shortener()
    for listing in response:
        listingDetails = response[listing]
        url = s.tinyurl.short(listingDetails['url'])
        stringResponse = stringResponse + '-----------<a href="'+url+'"> <b>Listing '+str(i)+'</b></a>-----------' + "\n<i>Name</i>: " + listingDetails['name']+ "\n<i>Rating</i>: " + listingDetails['rating']+ "\n<i>Price</i>: " + listingDetails['price']+ "\n<i>Apartment</i>: " + listingDetails['inventory']+ "\n"

        #Get venues based on coords
        coord = listingDetails['coordinates'].split(',')
        nearbyVenues = get_venues(coord[0], coord[1])
        venues = pd.DataFrame(nearbyVenues)
        
        stringResponse = stringResponse+'\n<u><i>Top 10 Venues near this listing</i></u>\n'
        
        #Create a map with folium then convert html to png
        create_folium_map(nearbyVenues, coord[0], coord[1], telegramChatID)
        convert_html_to_jpg()

        #Printing Venues
        for idx, venue in venues.iterrows():
            if (idx+1) >= len(venues.index):
                stringResponse = stringResponse + str(idx+1)+". " + venue[0].replace("&", "and") + " ("+venue[1]+")\n\n"
            else:
                stringResponse = stringResponse + str(idx+1)+". " + venue[0].replace("&", "and") +" ("+venue[1]+")\n"
        
        #Send text info
        if telegramChannel:
            telegram_bot_sendtext(stringResponse, telegramChatID)
        #Send images as an album
        telegram_bot_sendGroupMedia(listingDetails['picurl'][0:7], telegramChatID, i)

        i+=1
        stringResponse = ""
    telegram_bot_sendtext("\U0001F601 Search has been completed. Plese review our recommendations, thank you! \U0001F6C4\U00002708\U0001F3E1",telegramChatID)

def getDurationOfStay(fromDate, toDate):
    formattedDate = fromDate
    formattedDate = formattedDate.split("T")[0]    
    formattedDate = formattedDate.split("-")
    f_date = date(int(formattedDate[0]), int(formattedDate[1]), int(formattedDate[2]))

    formattedDate2 = toDate
    formattedDate2 = formattedDate2.split("T")[0]    
    formattedDate2 = formattedDate2.split("-")
    l_date = date(int(formattedDate2[0]), int(formattedDate2[1]), int(formattedDate2[2]))
    
    delta  = l_date - f_date
    return delta.days

def formatDate(date):
    formattedDate = date
    formattedDate = formattedDate.split("T")[0]    
    formattedDate = formattedDate.split("-")
    formattedDate = datetime.datetime(int(formattedDate[0]), int(formattedDate[1]), int(formattedDate[2]))
    formattedDate = formattedDate.strftime('X%d').replace('X0', '').replace('X','') +" "+ formattedDate.strftime('%B') +" "+ formattedDate.strftime('%Y')

    return formattedDate

def get_listing_coords(data):
    coords = []

    for listing in data:
        coords.append(listing['coordinates'])
    print("Coords are: "+str(coords))
    return coords 

def create_folium_map(venues, lati, longi, id):
    map = folium.Map([lati, longi], zoom_start=18,control_scale=True)

    i=0
    color = ["red","blue","green","gray","pink","darkred","darkpurple","orange","purple","cadetblue"]
    popup_text = ""
    
    folium.CircleMarker(location=(lati,
                                  longi),
                        radius= 20,
                        color="green",
                        text="1",
                        fill=True,
                        icon=DivIcon(
        icon_size=(150,36),
        icon_anchor=(7,20),
        html='<div style="font-size: 18pt; color : black">1</div>',
        )).add_child(folium.Popup("AirBnb", parse_html=True, show=True)).add_to(map)
    htmlText = ""
    for lat, lon, name, cat in zip(venues['Latitude'],venues['Longitude'], venues['Name'], venues['Category']):
        popup_text = popup_text.format(i,12,12)
        
        folium.Marker([lat, lon], popup='',icon=folium.Icon(color=color[i], icon='map-marker-alt')).add_to(map)
        htmlText = htmlText + '<li style="font-size:12px"><i class="fa fa-map-marker" style="color:'+color[i]+';font-size: 5em;"></i> '+name+' ('+cat+')</li>'
        i+=1
    template = get_legend_template(htmlText)
    macro = MacroElement()
    macro._template = Template(template)
    map.get_root().add_child(macro)
    
    map.save('./templates/map.html')

def get_venues(latitude, longitude):
    url = 'https://api.foursquare.com/v2/venues/explore'
    numberOfVenues = 10
    radius = 600 #in meters
    params = dict(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    v='20200401',
    ll=latitude+','+longitude,
    limit=numberOfVenues,
    radius = radius
    )
    resp = requests.get(url=url, params=params).json()
    
    venues = resp['response']['groups'][0]['items']

    nearby_venues = pd.DataFrame(columns=['Name', 'Category', 'Latitude', 'Longitude'])
    for venue in venues:
        df = pd.DataFrame([(venue['venue']['name'], 
                            venue['venue']['categories'][0]['name'],
                            venue['venue']['location']['lat'], 
                            venue['venue']['location']['lng'])], columns=['Name', 'Category', 'Latitude', 'Longitude'])
        nearby_venues = nearby_venues.append(df, ignore_index=True)
    print(nearby_venues.head())
    
    return nearby_venues

def telegram_bot_sendtext(bot_message, id):
    bot_chatID = str(id)
    response = bot.sendMessage(chat_id=bot_chatID, text=bot_message, disable_web_page_preview=True, parse_mode="html")

def telegram_bot_sendGroupMedia(bot_pic_URLs, id, listingNumber):
    imgArray = []
    bot_chatID = str(id)

    #Attach image URLs
    for idx, url in enumerate(bot_pic_URLs):
        if idx == 0:
            photo = telegram.InputMediaPhoto(media=url,caption="---------- End of listing "+str(listingNumber)+" ----------",parse_mode="markdown")
        else:
            photo = telegram.InputMediaPhoto(media=url,caption=None,parse_mode="markdown")
        imgArray.append(photo)
    
    photo1 = telegram.InputMediaPhoto(media=open('Images/map.jpg', 'rb'),caption=None)
    imgArray.append(photo1)

    response = bot.sendMediaGroup(chat_id=bot_chatID, media=imgArray, disable_notification=True)

def convert_html_to_jpg():
    URL = "http://127.0.0.1:5000/get_html" #localhost

    r.init()
    r.url(URL)
    print('Zooming out')
    r.click('//*[@class="leaflet-control-zoom-out"]')
    r.click('//*[@class="leaflet-control-zoom-out"]')
    print('Waiting to load...')
    r.wait(18)
       
    print('Snapping') 
    r.snap('//html/body',"./Images/map.jpg")
    print('Done.')

    r.close()

def get_legend_template(htmlText):
    template = '''
    {% macro html(this, kwargs) %}

<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>jQuery UI Draggable - Default functionality</title>
  <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">

  <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
  <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
  
  <script>
  $( function() {
    $( "#maplegend" ).draggable({
                    start: function (event, ui) {
                        $(this).css({
                            right: "auto",
                            top: "auto",
                            bottom: "auto"
                        });
                    }
                });
});

  </script>
</head>
<body>

 
<div id='maplegend' class='maplegend' 
    style='position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
     border-radius:6px; padding: 10px; font-size:14px; right: 20px; bottom: 20px;'>
     
<div class='legend-title'>Legend</div>
<div class='legend-scale'>
  <ul class='legend-labels'>'''

    template2 = ''' 
</ul>
</div>
</div>
 
</body>
</html>

<style type='text/css'>
  .maplegend .legend-title {
    text-align: left;
    margin-bottom: 5px;
    font-weight: bold;
    font-size: 90%;
    }
  .maplegend .legend-scale ul {
    margin: 0;
    margin-bottom: 5px;
    padding: 0;
    float: left;
    list-style: none;
    }
  .maplegend .legend-scale ul li {
    font-size: 80%;
    list-style: none;
    margin-left: 0;
    line-height: 18px;
    margin-bottom: 2px;
    }
  .maplegend ul.legend-labels li span {
    display: block;
    float: left;
    height: 16px;
    width: 30px;
    margin-right: 5px;
    margin-left: 0;
    border: 1px solid #999;
    }
  .maplegend .legend-source {
    font-size: 80%;
    color: #777;
    clear: both;
    }
  .maplegend a {
    color: #777;
    }
</style>
{% endmacro %}
'''

    template = template + htmlText + template2

    return template


# run Flask app
if __name__ == "__main__":
    app.run()