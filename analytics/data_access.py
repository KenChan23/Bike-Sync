# -*- coding: utf-8 -*-
"""
The script that facilitates the access to the data acquired

1. the pulse rate data from fitbit Charge HR
2. the historical data from the Citibike API
3. music data

Maybe we can create the class User to store information about the user
(e.g. bodyweight, bodyfat)


AWS command line
ssh changhl@ec2-54-172-195-184.compute-1.amazonaws.com

"""

import fitbit
from requests_oauthlib import OAuth1Session
import time
import pandas as pd
import boto3

client_key = '821263311ad14157876f1022010503af'
client_secret = '743e6d8e35b34088b3d4f2fabff85bb0'

class Fitbit:
    # the class Fitbit enables you to create the basic necessary user profile
    def __init__(self, client_key, client_secret):
        self.__fitbit_oAuth = fitbit.Fitbit(client_key, client_secret = client_secret)
        # as of now, Fitbit API deprecated the access to heart rate, blood pressure data
        self.__oAuth = OAuth1Session(client_key, client_secret = client_secret)
        
        # get the current date
        self.__currentDate = time.strftime("%Y-%m-%d")        
        
        # get the body weight
        self.__body_weight = self.__fitbit_oAuth.get_bodyweight()
        
        # get the body fat
        self.__body_fat = self.__fitbit_oAuth.get_bodyfat()
        
        # get daily activity track
        self.__daily_activity_json = self.getJsonData('http://GET /1/user/228TQ4/activities/date/' + self.__currentDate + '.json')
        
        # get the heart rate data formatted in json
        self.__heart_rate_json = self.getJsonData('http://GET /1/user/-/heart/date/'+self.__currentDate+'.json')
        
        # get the blood pressure data formatted in json
        self.__blood_pressure_json = self.getJsonData('http://GET /1/user/-/bp/date/'+ self.__currentDate+'.json')
    
    def getJsonData(self, url):
        jsonData = self.__oAuth.get(url)
        return jsonData
        
    def getAverageHeartRate(self):
        # use the json data from getHeartRateDataInJson to get the average heart rate
        # for a particular day
        # depending on the tracker status, we can see the heart rate
        # tracker status : "resting heart rate", "normal heart rate", "exertive heart rate", "running"
        averageHeartRate = self.__heart_rate_json["average"]
        averageHeartRate_df = pd.io.json.read_json(averageHeartRate)
        return averageHeartRate_df


    def getHeartRate(self):
        # use the json data from getHeartRateDataInJson to get the 
        heart_rates = self.__heart_rate_json["heart"]
        heart_rates_df = pd.io.json.read_json(heart_rates)
        return heart_rates_df
    
    def getAverageBloodPressure(self):
        averageBloodPressure = self.__blood_pressure_json["average"]
        averageBloodPressure_df = pd.io.json.read_json(averageBloodPressure)
        return averageBloodPressure_df
    
    def getBloodPressure(self):
        blood_pressure = self.__blood_pressure_json["bp"]
        blood_pressure_df = pd.io.json.read_json(blood_pressure)
        return blood_pressure_df
    
    """ design the methods for the activity as well as upload the data to AWS"""
    def getActivity(self):
        return 0
        
    def uploadToAWS(self):
    
# the data access for the citibike historical data from the AWS
class Citibike:
    
# the data access for the music from the AWS
class Music:

        
        
    
    
        
        

