import json
import geojson
import requests
from bson.objectid import ObjectId
from pymongo import MongoClient
from geojson import Feature, Point, FeatureCollection

# Define CRS object
crs = {
  "type": "name",
  "properties": {
    "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
  }
}

def connect():
# Substitute the 5 pieces of information you got when creating
# the Mongo DB Database (underlined in red in the screenshots)
# Obviously, do not store your password as plaintext in practice
    connection = MongoClient("ds062097.mongolab.com",62097)
    handle = connection["citibike"]
    handle.authenticate("root","root")
    return handle

handle = connect()

# Decode the encoded polyline
def decode_line(encoded):

  encoded_len = len(encoded)
  index = 0
  array = []
  lat = 0
  lng = 0

  while index < encoded_len:

      b = 0
      shift = 0
      result = 0

      while True:
          b = ord(encoded[index]) - 63
          index = index + 1
          result |= (b & 0x1f) << shift
          shift += 5
          if b < 0x20:
              break

      dlat = ~(result >> 1) if result & 1 else result >> 1
      lat += dlat

      shift = 0
      result = 0

      while True:
          b = ord(encoded[index]) - 63
          index = index + 1
          result |= (b & 0x1f) << shift
          shift += 5
          if b < 0x20:
              break

      dlng = ~(result >> 1) if result & 1 else result >> 1
      lng += dlng

      array.append((lat * 1e-5, lng * 1e-5))

  return array

# Generate appropriate JSON data for decoded polyline
def generatePointsJSON(decoded):

  time_counter = 0  
  # points = {'type': 'FeatureCollection', 'features': []}
  feature_list = []

  for latlng in decoded:
    time_counter += 1
    feature = Feature(geometry=Point((latlng[1], latlng[0])), properties={"latitude": latlng[0], "longitude": latlng[1], "time": time_counter, "id": "route", "city": "New York City", "state": "New York", "country": "US"})
    feature_list.append(feature)
  feature_collection = FeatureCollection(feature_list, crs=crs)
  return json.loads(geojson.dumps(feature_collection))
  # return (geojson.dumps(feature_collection))

def addGeoJSONAttribute(data_year):
    sample_counter = 0
    options = {
        "12-2014": {"data": list(handle._2014_12.find()), "collection": handle._2014_12, "sample": handle._2014_12_sample},
        "11-2014": {"data": list(handle._2014_11.find()), "collection": handle._2014_11, "sample": handle._2014_11_sample},
        "10-2014": {"data": list(handle._2014_10.find()), "collection": handle._2014_10, "sample": handle._2014_10_sample},
        "09-2014": {"data": list(handle._2014_09.find()), "collection": handle._2014_09, "sample": handle._2014_09_sample},
        "08-2014": {"data": list(handle._2014_08.find()), "collection": handle._2014_08, "sample": handle._2014_08_sample},
        "07-2014": {"data": list(handle._2014_07.find()), "collection": handle._2014_07, "sample": handle._2014_07_sample},
        "06-2014": {"data": list(handle._2014_06.find()), "collection": handle._2014_06, "sample": handle._2014_06_sample},
        "05-2014": {"data": list(handle._2014_05.find()), "collection": handle._2014_05, "sample": handle._2014_05_sample},
        "04-2014": {"data": list(handle._2014_04.find()), "collection": handle._2014_04, "sample": handle._2014_04_sample},
        "03-2014": {"data": list(handle._2014_03.find()), "collection": handle._2014_03, "sample": handle._2014_03_sample},
        "02-2014": {"data": list(handle._2014_02.find()), "collection": handle._2014_02, "sample": handle._2014_02_sample},
        "01-2014": {"data": list(handle._2014_01.find()), "collection": handle._2014_01, "sample": handle._2014_01_sample},
        "12-2013": {"data": list(handle._2013_12.find()), "collection": handle._2013_12, "sample": handle._2013_12_sample},
        "11-2013": {"data": list(handle._2013_11.find()), "collection": handle._2013_11, "sample": handle._2013_11_sample},
        "10-2013": {"data": list(handle._2013_10.find()), "collection": handle._2013_10, "sample": handle._2013_10_sample},
        "09-2013": {"data": list(handle._2013_09.find()), "collection": handle._2013_09, "sample": handle._2013_09_sample},
        "08-2013": {"data": list(handle._2013_08.find()), "collection": handle._2013_08, "sample": handle._2013_08_sample}
    }
    for d in options[data_year]["data"]:
      if sample_counter < 100:
        encodedData = getEncodedString(d)
        if encodedData != 'null': 
          geoJSONData = generatePointsJSON(decode_line(encodedData))
          # options[data_year]["collection"].update({"_id": ObjectId(str(d["_id"]))}, {"$set": {"geoData": geoJSONData}})
          oldData = options[data_year]["collection"].find_one({"_id": ObjectId(str(d["_id"]))})
          options[data_year]["sample"].insert(oldData)
          options[data_year]["sample"].update({"_id": ObjectId(str(d["_id"]))}, {"$set": {"geoData": geoJSONData}})
          sample_counter += 1
        else:
          # options[data_year]["collection"].update({"_id": ObjectId(str(d["_id"]))}, {"$set": {"geoData": 'null'}})
          continue
      else:
        print "Finished getting 100 samples for web application."
        break

def getEncodedString(d):
  url = "https://maps.googleapis.com/maps/api/directions/json?origin=" + d["start station latitude"] + "," + d["start station longitude"] + "&destination=" + d["end station latitude"] + "," + d["end station longitude"]
  try:  
    response = requests.get(url)
    data = response.json()
    data = data["routes"][0]["overview_polyline"]["points"]
  except IndexError:
    data = 'null'
  print data
  return data
  # print type(data["routes"][0]["overview_polyline"]["points"])
  # return data["routes"][0]["overview_polyline"]["points"]

if __name__ == "__main__":

  # latlngs = decode_line("k~wwFxlrbMrGhErAz@lA{DhKk\zEeO|@yCnJeZjCcIh@eBzA{E`GxDlNfJdKxGtFvDxFpD|I~F")
  # generatePointsJSON(latlngs)
  addGeoJSONAttribute("10-2014")
