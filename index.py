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
sys.path.insert(0,'./Source/tagui-v1.3/')
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
from werkzeug.serving import WSGIRequestHandler

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
    
    response = airbnb.process(country, int(numOfAdults), int(numOfInfants), int(numOfChildren), fromDate, toDate)
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
        print("Retrieving next coords...")
        listingDetails = response[listing]
        print("Shortening URL...")
        convertedURL = False
        while convertedURL == False:
            try:
                url = s.tinyurl.short(listingDetails['url'])
                convertedURL = True
                print("Successfully converted URL...")
            except Exception as ex:
                print("Error shortening URL, retrying...")
        
        stringResponse = stringResponse + '-----------<a href="'+url+'"> <b>Listing '+str(i)+'</b></a>-----------' + "\n<i>Name</i>: " + listingDetails['name']+ "\n<i>Rating</i>: " + listingDetails['rating']+ "\n<i>Price</i>: " + listingDetails['price']+ "\n<i>Apartment</i>: " + listingDetails['inventory']+ "\n"

        #Get venues based on coords
        print("Getting Venues...")
        coord = listingDetails['coordinates'].split(',')
        nearbyVenues = get_venues(coord[0], coord[1])
        venues = pd.DataFrame(nearbyVenues)
        
        stringResponse = stringResponse+'\n<u><i>Top Venues near this listing</i></u>\n'
        
        #Create a map with folium then convert html to png
        print("Creating Folium map...")
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
            print("Sending telegram text...")
            telegram_bot_sendtext(stringResponse, telegramChatID)
        #Send images as an album
        print("Sending telegram group pics...")
        telegram_bot_sendGroupMedia(listingDetails['picurl'][0:7], telegramChatID, i)
        print("Done sending telegram group pics...")
        i+=1
        stringResponse = ""
    time.sleep(10)
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
    
    foursquareError = False
    while foursquareError == False:
        try:
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
            foursquareError = True
        except Exception as ex:
            print("Foursquare API Error... Retrying...")

    return nearby_venues

def telegram_bot_sendtext(bot_message, id):
    try:
        bot_chatID = str(id)
        response = bot.sendMessage(chat_id=bot_chatID, text=bot_message, disable_web_page_preview=True, parse_mode="html")
    except Exception as ex:
        print("Telegram text error...")

def telegram_bot_sendGroupMedia(bot_pic_URLs, id, listingNumber):
    try:
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
    except Exception as ex:
        print("Telegram group photo error...")

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
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    app.run()