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
from Analytics import pygn
from pandas import read_json

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
        print request.json['data']
        return request.json['data']
        # data = request.json['data']
        ##  Using a form requires the request.form function
        # print data

@app.route('/recommendation', methods=["POST"])
def recommendation():
    print "Inside views.py under recommendation"
    if request.method == "POST":
        ls = []
        for song in request.json:
            a_metadata = pygn.search(clientID = "58624-530E5E2D845DB16CB7D3A258CCCD5E07",
                                    userID = "27396709641709153-2C0CF7D92465CE0CC6B7DC560EFCE44E",
                                    artist = song['songArtist'],
                                    album = song['songAlbum'],
                                    track = song['songTitle'])
            a_metadata['songID'] = song['songID'] 
            ls.append(a_metadata)

        music_data = read_json(ls)
        content = main.main(music_data)

        # return request.json['data']
        # data = request.json['data']
        ##  Using a form requires the request.form function
        # print data
        # resp = Response(response=, status=200, mimetype="application/json")
        response = Response(response=content, status=200, mimetype="application/json")
    return (response)
