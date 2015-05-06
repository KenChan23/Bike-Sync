"""
	output_recommended_songs.py
	the script runs the POST request method to output the recommended songs to the route called
	output_recommended_songs
"""
import requests
import json
import urllib
import urllib2

url = 'http://localhost:8000/output_recommended_songs'

json_file = open("./MusicRecommendation/recommended_songs.json", 'r')
payload = json_file.readline()
payload = json.loads(payload)

data = urllib.urlencode(payload)
request = urllib2.Request(url, json.dumps(payload), headers = headers)
request.add_header("content-type","application/json")
response = urllib2.urlopen(request)