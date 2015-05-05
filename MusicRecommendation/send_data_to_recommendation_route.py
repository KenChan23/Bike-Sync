import requests
import json
import urllib
import urllib2

url = 'http://localhost:8000/recommendation'

json_file = open("recommended_songs.json", 'r')
payload = json_file.readline()
payload = json.loads(payload)

data = urllib.urlencode(payload)
print data
request = urllib2.Request(url, json.dumps(payload))
request.add_header("content-type","application/json")
print request
response = urllib2.urlopen(request)

#headers = {'content-type': 'application/json'}
#response = requests.post(url, data=json.dumps(payload), headers=headers)
