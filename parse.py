import os
import pprint
import csv
from pymongo import MongoClient

DATADIR = "data/"
DATAFILE = [
            "2014-10-citibike-tripdata.csv", \
            "2014-11-citibike-tripdata.csv", \
            "2014-12-citibike-tripdata.csv" \
           ]

def connect():
    connection = MongoClient("ds062097.mongolab.com",62097)
    handle = connection["citibike"]
    handle.authenticate("root","root")
    return handle

def parse_csv(datafile, filename, handle):
  data = []
  n = 0
  with open(datafile, 'rb') as sd:
    r = csv.DictReader(sd)
    for line in r:
      data.append(line)
      pprint.pprint(line)
      if filename[0:7] == "2014-10":
        handle._2014_10.insert(line)
      if filename[0:7] == "2014-11":
        handle._2014_11.insert(line)
      if filename[0:7] == "2014-12":
        handle._2014_12.insert(line)
  return data

if __name__ == '__main__':
  # Connect to MongoDB hosted on MongoLabs
  handle = connect()
  # Iterate through each .csv file
  # Store contents into corresponding collection
  for filename in DATAFILE:
    datafile = os.path.join(DATADIR, filename)
    d = parse_csv(datafile, filename, handle)
    pprint.pprint(d)