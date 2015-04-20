"""
	music_recommendation.py

"""

import pickle
import pygn
import pandas as pd
from math import hypot
from re import sub
# from textblob import TextBlob
import os
os.system("alchemypapi.py e2cbc188993e799390a9b9cf510c3927df0b2279")
from alchemyapi import AlchemyAPI
alchemy_obj = AlchemyAPI()


#Register pygn with client id. This is in a separate file to be used once per end user because
#each call to pygn.register goes towards a quota. We will need to run this for each user
#and store their UserID in our database. Then, we can query each song individually and store
#it's metadata in our database.


# each tuple = (arousal, valence)
av_chart = {(22.5, 67.5):'excitment',
            (67.5, 112.5):'arousal',
            (112.5, 157.5):'distress',
            (157.5, 202.5):'displeasure',
            (202.5, 247.5):'depression',
            (247.5,292.5):'sleepiness',
            (292.5,337.5):'relaxation',
            (337.5, 22.5):'pleasure'}
            
def register():

    gracenoteClientID = "58624-530E5E2D845DB16CB7D3A258CCCD5E07"
    gracenoteUserID = pygn.register(gracenoteClientID)

    return gracenoteUserID

gracenoteClientID = "58624-530E5E2D845DB16CB7D3A258CCCD5E07"
sampleUserID = "27396709641709153-2C0CF7D92465CE0CC6B7DC560EFCE44E"

def gracenoteSearch(user, album, artist, song):
    # the function used for calling all the metadata about the music in the user's playlist
    # this function is using the gracenote API to retrieve the information
    return pygn.search(clientID=gracenoteClientID, userID = user, artist=artist, album=album, track=song)


def getTempo(record):
    # this function will be used for extracting the tempo and mood of each music record
    
    # Parameter
    # record : a dictionary whose keys are as follows:
    # 'track_title', 'album_year', 'tempo', 'track_gnid', 'artist_image_url', 'tracks', 'genre', 
    # 'album_artist_name', 'track_artist_name', 'xid', 'mood', 'artist_bio_url', 'album_art_url', 
    # 'radio_id', 'track_number', 'artist_era', 'album_gnid', 'artist_origin', 'album_title', 
    # 'review_url', 'artist_type'
    
    # Returns
    # the new data frame whose columns are 'tempo' and 'mood'. The new data frame will be appended

    tempo = record['tempo']
    return tempo

def getMood(record):
    # same technique for getting the mood data from the data_df['gnresult']

    mood = record['mood']
    return mood

def getTextualValue(record):
    # similar to the function getQuantifiedValueofTempo, but this time
    # it extracts the information about the Text part describing the tempo
    
    # Parameter
    # record : one record of tempo
    # Returns: the changed value of the tempo that contains the list of textual value
    
    value_str_one = record['1']['TEXT']
    value_str_two = record['2']['TEXT']
        
    return [value_str_one, value_str_two]

def getQuantifiedValueofTempo(record):
    # get the quantified value of the tempo
    # record is a dictionary, and the value we are looking for is located in
    # the value whose key is 3
    # will be used as lambda function
    # e.g.
    # {'1': {'ID': '34283', 'TEXT': 'Medium Tempo'},
    # '2': {'ID': '34291', 'TEXT': 'Medium Fast'},
    # '3': {'ID': '34318', 'TEXT': '90s'}}
    
    # Parameter
    # record : one record of tempo
    # Returns: the changed values of the tempo
    
    value_str = record['3']['TEXT'] # formatted as 'XXXs'
    val = int(value_str[0:len(value_str)-1]) # substring such that you only get the numerical value
        
    return val

def getMusicData(filename):
    # get the metadata about the musics using the Gracenote API
    # and change this into DataFrame
    
    # Parameter
    # filename : the name of the file containing the metadata about the musics
    
    # Returns
    # the data frame that has the necessary information about music
    
    raw_data_dic = pickle.load(open(filename,'r'))

    data_dic = raw_data_dic['data']
    data_df = pd.DataFrame.from_dict(data_dic)
    
    data_df['tempo'] = data_df['gnresult'].apply(lambda x: getTempo(x))
    data_df['mood'] = data_df['gnresult'].apply(lambda x: getMood(x))
    
    # if tempo is empty, then mood is empty too
    data_df = data_df[data_df['tempo']!={}]
    
    data_df['tempo_val'] = data_df['tempo'].apply(lambda x: getQuantifiedValueofTempo(x))
    data_df['tempo_text'] = data_df['tempo'].apply(lambda x: getTextualValue(x))
    data_df['mood_text'] = data_df['mood'].apply(lambda x: getTextualValue(x))
    
    del data_df['gnresult']
    del data_df['mood']
    del data_df['tempo']
    
    return data_df


def quantify_mood_text(mood_list):
    # quantify the textual description of the mood using AlchemyAPI sentiment analysis technique
    # Parameter:
    # mood_list : the list that contains the words describing the mood of the music
    # Returns
    # sentiment_score : the aggregated score of the sentiment extracted from the word
    
    # get the list of the words from the string
    get_words = []
    for words in mood_list:
        extra_words = words.split(" / ")
        for word in extra_words:
            get_words.append(word)
    
    sentiment_score = 0.0
    for word in set(get_words):
        response = alchemy_obj.sentiment("text", word)
        if(response.has_key('docSentiment')):
            if (response['docSentiment'].has_key('score')):
                a_score = response['docSentiment']['score']
                sentiment_score = sentiment_score + float(a_score)
                
    # sentiment_score  = sentiment_score / float(len(mood_list))
    # scale it into a range between 0 and 200
    
    sentiment_score = 100*(sentiment_score-(-1)/(1-(-1)))
    
    return sentiment_score
        