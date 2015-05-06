# mongo ec2-54-172-195-184.compute-1.amazonaws.com/citibike -u kenchan -p root

# import json
import os
from pymongo import MongoClient
from datetime import datetime
from flask import Flask, Response, render_template, request, redirect, jsonify
from flask import json
from bson import json_util
from bson.objectid import ObjectId
from MusicRecommendation import app
from Analytics import main
import pandas as pd

HOSTNAME = "ec2-54-172-195-184.compute-1.amazonaws.com"
DATABASE = "citibike"
USERNAME = "kenchan"
PASSWORD = "root"

def connect():
# Substitute the 5 pieces of information you got when creating
# the Mongo DB Database (underlined in red in the screenshots)
# Obviously, do not store your password as plaintext in practice
    connection = MongoClient("ds062097.mongolab.com",62097)
    handle = connection["citibike"]
    handle.authenticate("root","root")
    print "Connected"
    return handle

handle = connect()

def retrieve_data(quantity, data_year):
    options = {
        "12-2014": list(handle._2014_12.find().limit(int(quantity))),
        "11-2014": list(handle._2014_11.find().limit(int(quantity))),
        "10-2014": list(handle._2014_10.find().limit(int(quantity))),
        "09-2014": list(handle._2014_09.find().limit(int(quantity))),
        "08-2014": list(handle._2014_08.find().limit(int(quantity))),
        "07-2014": list(handle._2014_07.find().limit(int(quantity))),
        "06-2014": list(handle._2014_06.find().limit(int(quantity))),
        "05-2014": list(handle._2014_05.find().limit(int(quantity))),
        "04-2014": list(handle._2014_04.find().limit(int(quantity))),
        "03-2014": list(handle._2014_03.find().limit(int(quantity))),
        "02-2014": list(handle._2014_02.find().limit(int(quantity))),
        "01-2014": list(handle._2014_01.find().limit(int(quantity))),
        "12-2013": list(handle._2013_12.find().limit(int(quantity))),
        "11-2013": list(handle._2013_11.find().limit(int(quantity))),
        "10-2013": list(handle._2013_10.find().limit(int(quantity))),
        "09-2013": list(handle._2013_09.find().limit(int(quantity))),
        "08-2013": list(handle._2013_08.find().limit(int(quantity)))
    }
    return options[data_year]

def retrieve_sample(data_year, index):
    options = {
        "12-2014": list(handle._2014_12_sample.find({"index": int(index)})),
        "11-2014": list(handle._2014_11_sample.find({"index": int(index)})),
        "10-2014": list(handle._2014_10_sample.find({"index": int(index)})),
        "09-2014": list(handle._2014_09_sample.find({"index": int(index)})),
        "08-2014": list(handle._2014_08_sample.find({"index": int(index)})),
        "07-2014": list(handle._2014_07_sample.find({"index": int(index)})),
        "06-2014": list(handle._2014_06_sample.find({"index": int(index)})),
        "05-2014": list(handle._2014_05_sample.find({"index": int(index)})),
        "04-2014": list(handle._2014_04_sample.find({"index": int(index)})),
        "03-2014": list(handle._2014_03_sample.find({"index": int(index)})),
        "02-2014": list(handle._2014_02_sample.find({"index": int(index)})),
        "01-2014": list(handle._2014_01_sample.find({"index": int(index)})),
        "12-2013": list(handle._2013_12_sample.find({"index": int(index)})),
        "11-2013": list(handle._2013_11_sample.find({"index": int(index)})),
        "10-2013": list(handle._2013_10_sample.find({"index": int(index)})),
        "09-2013": list(handle._2013_09_sample.find({"index": int(index)})),
        "08-2013": list(handle._2013_08_sample.find({"index": int(index)}))
    }
    return options[data_year]

@app.route("/api/12-2014/<quantity>", methods=['GET'])
def get_12_2014(quantity):
    return json.dumps(retrieve_data(quantity, "12-2014"), default=json_util.default)

@app.route("/api/11-2014/<quantity>", methods=['GET'])
def get_11_2014(quantity):
    return json.dumps(retrieve_data(quantity, "11-2014"), default=json_util.default)

@app.route("/api/10-2014/<quantity>", methods=['GET'])
def get_10_2014(quantity):
    return json.dumps(retrieve_data(quantity, "10-2014"), default=json_util.default)

@app.route("/api/09-2014/<quantity>", methods=['GET'])
def get_09_2014(quantity):
    return json.dumps(retrieve_data(quantity, "09-2014"), default=json_util.default)

@app.route("/api/08-2014/<quantity>", methods=['GET'])
def get_08_2014(quantity):
    return json.dumps(retrieve_data(quantity, "08-2014"), default=json_util.default)

@app.route("/api/07-2014/<quantity>", methods=['GET'])
def get_07_2014(quantity):
    return json.dumps(retrieve_data(quantity, "07-2014"), default=json_util.default)

@app.route("/api/06-2014/<quantity>", methods=['GET'])
def get_06_2014(quantity):
    return json.dumps(retrieve_data(quantity, "06-2014"), default=json_util.default)

@app.route("/api/05-2014/<quantity>", methods=['GET'])
def get_05_2014(quantity):
    return json.dumps(retrieve_data(quantity, "05-2014"), default=json_util.default)

@app.route("/api/04-2014/<quantity>", methods=['GET'])
def get_04_2014(quantity):
    return json.dumps(retrieve_data(quantity, "04-2014"), default=json_util.default)

@app.route("/api/03-2014/<quantity>", methods=['GET'])
def get_03_2014(quantity):
    return json.dumps(retrieve_data(quantity, "03-2014"), default=json_util.default)

@app.route("/api/02-2014/<quantity>", methods=['GET'])
def get_02_2014(quantity):
    return json.dumps(retrieve_data(quantity, "02-2014"), default=json_util.default)

@app.route("/api/01-2014/<quantity>", methods=['GET'])
def get_01_2014(quantity):
    return json.dumps(retrieve_data(quantity, "01-2014"), default=json_util.default)

@app.route("/api/12-2013/<quantity>", methods=['GET'])
def get_12_2013(quantity):
    return json.dumps(retrieve_data(quantity, "12-2013"), default=json_util.default)

@app.route("/api/11-2013/<quantity>", methods=['GET'])
def get_11_2013(quantity):
    return json.dumps(retrieve_data(quantity, "11-2013"), default=json_util.default)

@app.route("/api/10-2013/<quantity>", methods=['GET'])
def get_10_2013(quantity):
    return json.dumps(retrieve_data(quantity, "10-2013"), default=json_util.default)

@app.route("/api/09-2013/<quantity>", methods=['GET'])
def get_09_2013(quantity):
    return json.dumps(retrieve_data(quantity, "09-2013"), default=json_util.default)

@app.route("/api/08-2013/<quantity>", methods=['GET'])
def get_08_2013(quantity):
    return json.dumps(retrieve_data(quantity, "08-2013"), default=json_util.default)

## Sample end-points for rendering visualization
# 54ef556ccbbe69683aa68197
@app.route("/api/sample/10-2014/<index>", methods=['GET'])
def get_10_2014_sample(index):
    return json.dumps(retrieve_sample("10-2014", index), default=json_util.default)

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Bike-Sync',
        year=datetime.now().year,
    )

@app.route('/load_date_data', methods=["POST"])
def load_data():
    if request.method == "POST":


        return request.json['data']
        # data = request.json['data']
        ##  Using a form requires the request.form function
        # print data

@app.route('/recommendation', methods=["POST"])
def recommendation():
    # this route makes the recommendatiaon of songs using the music data that is sent from
    # the android music player (POST request)

    if request.method == "POST":
        print request.json

        # get the music data from Android app t
        all_music_data = ad.DataFrame.read_dict(request.json)
        # makes recommendations based on the music data as well as other data souces
        payload = main.main(all_music_data) 
        # will write the output of the recommended songs to the disk (.json format)

        response = Response(response=payload, status=200, mimetype="application/json")
    return (response)

@app.route('/output_recommended_songs', methods = ["POST"])
def output_recommended_songs():
    # this route calls the output_recommended_songs.py in order to make POST request
    # to send the recommended songs data to the route

    print "outputting the recommended songs worked!"
    if request.method == "POST":
        print request.json['data']
        response = Response(response=request.json['data'], status=200, mimetype="application/json")
        return (response)



