"""
	music_recommendation.py

"""

import pickle
import pygn
import pandas as pd
# from textblob import TextBlob
import os
os.system("alchemypapi.py e2cbc188993e799390a9b9cf510c3927df0b2279")
from alchemyapi import AlchemyAPI
alchemy_obj = AlchemyAPI()
from textblob import TextBlob
import preprocessing

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
            
# the sentiment score of the av_chart using AlchemyAPI
# as a result, you will get the following scores
av_chart_scores = {'arousal': 56.327000000000005,
                   'depression': 19.394299999999998,
                   'displeasure': 39.192899999999995,
                   'distress': 34.732149999999997,
                   'excitment': 72.7881,
                   'pleasure': 79.759650000000008,
                   'relaxation': 69.67649999999999,
                   'sleepiness': 20.901700000000002}

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
                
    sentiment_score  = sentiment_score / float(len(mood_list))
    # scale it into a range between 0 and 200
    
    sentiment_score = preprocessing.scale(sentiment_score,-1, 1, 0, 100)
    
    return sentiment_score
 

def categorize_music(av_chart_scores, mood_score):
    # using the sentiment score data structures for the AV model and the data from the Gracenote API,
    # categorize the musics by comparing the scores
    # Approach : categorize the songs whose scores are close to the score of each category
    # of the AV model
    # find out the difference between each score of the AV model and mood_score
    # and assign the label whose absolute value of score difference is the minimum

    # Paramter:
    # av_chart_score : the sentiment score of the labels of the AV model
    # mood_score : the single invididual score of one music piece

    # Returns
    # a_word : the label from the AV model whose sentiment score is very close to the score
    # of the music's mood

    diff = 100
    label = av_chart_scores.keys()[0]
    for a_word in av_chart_scores.keys():
        diff_temp = abs(av_chart_scores[a_word]-mood_score)
        if (diff_temp < diff):
            diff = diff_temp
            label = a_word
    
    return label

def get_predicted_music_label(av_chart_scores, music_data_mood_score):
    # use the categorize_music function to get the predicted music label
    # the lambda function technique is used in this function
    
    # Paramter:
    # av_chart_score : the sentiment score of the labels of the AV model
    # music_data_mood_score : the DataFrame of music data
    
    # Returns
    # pred_labels : the DataFrame object containing the predicted music labels
    
    pred_labels =  music_data_mood_score.apply(lambda x: categorize_music(av_chart_scores, x))
    
    return pred_labels

def create_data_structure(music_data):
    # using the music_data, the function groups by the pred_labels
    # and it will give you the dictionary whose key is the label and whose value is the list
    # of the records indicated by the indices in the music_data
    
    # then, the grouped data structure will grap each element in the list and store the index
    # as well as the sentiment score of the music piece in the data structure
    
    # Paramter:
    # music_data : the DataFrame of the music piece
    
    # Returns
    # The data structure
    
    groupd_obj = music_data.groupby('pred_labels').groups
    
    # create the data structure that has the scores
    for word in groupd_obj:
        
        for i in range(0, len(groupd_obj[word])):
            index = groupd_obj[word][i]
            score = music_data.loc[index, 'mood_score']
            groupd_obj[word][i] = (index, score)
    
    return groupd_obj
    

def get_most_popular_emotion(emotion_labels):
    # get the most popular emotions
    return 0

def map_from_emotion_to_music_label(emotion_labels, groupd_obj):
    # using the predicted emotion label (the emotioanl state of the user) and the already made
    # data structure that has categorized the music according to the music labels,
    # it recommends the songs 

    # Paramter
    # emotion_labels : the Series object taht has current 20 ~ 25 predicted emotional labels 
    # groupd_obj : the data structure that has all the categorization of the music

    # Returns
    # label_of_recoomend_songs : the label of the group of songs that is recommended to the user
    
    # Approach :
    # get the most predicted labels out of all the data from emotion_labels
    # and make recommendations according to the most popular emotion
    
    most_popular_emotion = emotion_labels.value_counts().index[0] 
    # .value_counts() always sorts out in descending order, so the one in the zeroth index is the most popular one
    
    if (most_popular_emotion is 'distress' or most_popular_emotion is 'displeasure' or most_popular_emotion is 'depression'):
        label_of_recommended_songs = 'pleasure'
        
    if (most_popular_emotion is 'pleasure'):
        label_of_recommended_songs = 'excitement'
        
    if (most_popular_emotion is 'arousal'):
        label_of_recommended_songs = 'relaxation'
    
    if (most_popular_emotion is 'relaxation'):
        label_of_recommended_songs = 'pleasure'
    
    if (most_popular_emotion is 'sleepiness'):
        label_of_recommended_songs = 'arousal'
    
    return label_of_recommended_songs


def get_songs_from_label(label_of_recommended_songs, groupd_obj, music_data):
    # get the label of the recommended songs and output the informaiton of the recommended songs to the json file

    # Parameter
    # label_of_recommended_songs : the recommended emotional label that has the songs
    # groupd_obj : the data structure that has the categorization of the songs
    # music_data : the data frame  that has the information about the music

    
    recommended_songs = groupd_obj[label_of_recommended_songs][0:2]
    ls_index = []
    for a_tuple in recommended_songs:
        an_id = a_tuple[0]
        ls_index.append(an_id)
    
    records = music_data.iloc[ls_index]
    records.to_json('recommended_songs.json', orient='records')

    

        