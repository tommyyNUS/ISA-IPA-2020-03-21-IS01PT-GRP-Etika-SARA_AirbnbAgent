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

app = Flask(__name__)

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
        
    response = airbnb.process(country, int(numOfAdults), int(numOfInfants), int(numOfChildren), fromDate, toDate)

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

# run Flask app
if __name__ == "__main__":
    app.run()