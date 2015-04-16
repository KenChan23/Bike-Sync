"""
	music_recommendation.py

"""


"""

	Let's Get Physical: The Psychology of Effective Workout Music
	http://www.scientificamerican.com/article/psychology-workout-music/

	
	pop, hip-hop, alternative, rock, dance,  --> makes your heart beat faster

	blues, reggae, classics, --> makes your heartbeat at rest

	country music --> can make you feel depressed

	meditation -> reduce stress and put your heartbeat at ease

"""

"""
	the way to approach : learn the features of the music, especially the tempo
	and link this to the sentiment
	the link between the tempo and the music

	how do you build the top-k scoring functions for music based on the genres?

"""

"""
    Resonance-Valence-Arousal Systems
"""

"""
genre-based
"""
import pickle
import pygn
import pandas as pd

#Register pygn with client id. This is in a separate file to be used once per end user because
#each call to pygn.register goes towards a quota. We will need to run this for each user
#and store their UserID in our database. Then, we can query each song individually and store
#it's metadata in our database.

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