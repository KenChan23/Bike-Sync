import pyowm
from datetime import datetime
import pandas as pad
import time

owm = pyowm.OWM('67b42756a45f998b9ecdeb0b03f9ed31')

# New York's ID = 5128581
observation = owm.weather_at_place('New York, USA')

aFile = open("weather.txt", 'a')
aFile.write('[')

while(True):
	# the time
	now = datetime.now()

	year = now.year
	month = now.month
	day = now.day
	hr = now.hour
	minute = now.minute
	sec = now.second

	w = observation.get_weather()

	wind_dic = w.get_wind()
	wind_speed = wind_dic['speed']
	wind_deg = wind_dic['deg']

	humidty = w.get_humidity() 

	temp_dic = w.get_temperature('celsius')  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}
	temp_max = temp_dic['temp_max']
	temp = temp_dic['temp']
	temp_min = temp_dic['temp_min']

	dic = {'year':year, 'month': month, 'day': day, 'hr' : hr, 'minute': minute, 'sec':sec,
		'wind_speed':wind_speed, 'wind_deg':wind_deg, 'humidity':humidty, 
		'temp_max':temp_max,'temp':temp, 'temp_min':temp_min}

	# write to AWS
	aFile.write(str(dic)+",")


	time.sleep(60)

aFile.write("]")

aFile.close()







