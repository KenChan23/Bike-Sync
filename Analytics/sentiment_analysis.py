"""
    sentiment_analysis.py
"""
import pandas as pd
import random
import sklearn as ml
import sklearn.cluster as clustering
import collections
import preprocessing
from math import atan
from math import pi
from os import system
system("python alchemyapi.py e2cbc188993e799390a9b9cf510c3927df0b2279")
from alchemyapi import AlchemyAPI
alchemy_obj = AlchemyAPI()

# the mood category used for clustering
mood_category = {1:"neutral", 2:"sad", 3:"happy", 4:"angry", 5:"anxious"}

# the AV-chart to predict the user's sentiment
# key : the range of angle values
# value : the label of emotions
av_chart = {(22.5, 67.5):'excitement',
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
                   'excitement': 72.7881,
                   'pleasure': 79.759650000000008,
                   'relaxation': 69.67649999999999,
                   'sleepiness': 20.901700000000002}


def featureExtractActivity(data, random_sample_size):
    # extracts the features from the dataset whose data instance is the Activity instance
    # for each second, randomly select 50 samples from the whole dataset
    # randmoly generate numbers between 0 and the size of the accleration_df 
    # with the size of random_sample_sizes
    idx = []
    for i in range(random_sample_size):
        idx.append(random.randint(0,data.itemsize()))
        
    return idx


def activity_cluster(idx, data_df, n_clusters):
    # exectue the k-means clustering algorithm and returns the newly made labels 
    # n_clusters can be adjusted based upon the user's request

    # extract the features by extracting only a small sample of the dataset
    random_features = data_df[idx]
    # run the k-means clustering algorithm to cluster the randomly selected features
    k_means_obj = ml.cluster.KMeans(n_clusters)
    k_means_obj.fit(random_features)
    return k_means_obj.predict(random_features)
    
    
def activity_classfication(labels, user_data, idx):
    # use the labels obtained from the k-means clustering and user's data to classify the user's activty
    # here, we use the random forest classifier
    needed_data = user_data[idx]
    classifier_obj = ml.ensemble.RandomForestClassifier()
    classifier_obj.fit(needed_data, labels)
    
    pred_values = classifier_obj.predict(needed_data)
    return pred_values


def predict_user_activity(pred_values):
    # using the predicted value of the user's activity over the T seconds,
    # predict the user's current activity level
    # here, we use the voting techinque (pick out the most freuquent activity label)
    # use the collections library to count the most frequently produced activity level among
    # all the labels
    
    return collections.Counter(pred_values).most_common()[0]


""" 
HEART RATE-BASED SENTIMENT ANALYSIS 

REFERENCE
    - Muhammad Tauseef Quazi, Human Emotion Recognition Using Smart Sensors,
    School of Engineering and Advanced Technology, Massey University (2012)

"""

# Happy, Sad, Neutral, and Angry
# according to the paper, the heart rate is in the following order
# neutral < sad < happy < angry


def determine_emotion(one_record, emotions_range):
    # using the preb_labels's data, predict the emotion
    for a_range in emotions_range.keys():
        if(one_record >= a_range[0] and one_record <= a_range[1]):
            pred_emotion = emotions_range[a_range]
    
    return pred_emotion


def data_cluster(data_df, n_emotions):
    # using the data_df, it clusters into the group of emotions indicated by n_emotions
    # and using the new data that is coming, it gives you the predicted labels 
    # and return the data frame as well as the label in it

    #sdata_df = preprocessing.normalize(data_df)
    #data_sf = SFrame(data_df) # turn this into SFrame
    #k_means_obj = kmeans.create(data_sf, num_clusters = n_emotions)
    
    k_means_obj = clustering.KMeans(n_emotions)
    k_means_obj.fit(data_df)
    
    k_means_obj.cluster_centers_.sort(axis=0)
    
    cluster_centers = pd.DataFrame(k_means_obj.cluster_centers_)
    
    # using the sorted ndarray, make the predicted emotions range
    pred_emotions_range = {}
    for i in range(0, len(cluster_centers[0])):
        if (i+1 != len(cluster_centers[0])):
            key = (cluster_centers[0][i], cluster_centers[0][i+1])
        else:
            key = (cluster_centers[0][i], 'infinity')
        
        pred_emotions_range[key] = i+1
    
    return pred_emotions_range, k_means_obj


def calculate_angle(data_record):
    # the function to estimate the angle of the line laying in the 2D coordinate
    # the function will be used to estimate the AV value and predict the emotions
    
    # Paramter:
    # data_record : ONE instance of data whose number of columns is 2
    # Returns
    # angle : the estimated angle
    
    # get x and y coordinates
    x = data_record[0] # beats per minute
    y = data_record[1] # calories burned
        
    # get the angle measure using python library
    angle = 180/pi*atan(y/x)
    
    # if the angle is less than 0, then add 360 to make it positive
    if (angle < 0): angle = angle + 360
    
    return angle
    

def get_predicted_labels_using_angles(pred_angle):
    # use the av_chart score to predicte the emotional state
    
    # Parameter
    # pred_angle : the float value of an angle representing the labels of the emotioanal state.
    # Returns
    # the predicted label of type string that is mapped from the angle range.
    # if not found, it returns -1
    
    for an_angle_range in av_chart.keys():
        if (pred_angle >= an_angle_range[0] and pred_angle < an_angle_range[1]):
            return av_chart[an_angle_range]
            
    return -1
    

def predict_emotion_using_AV_model(data_df):
    # using Russell's Arousal-Valence model, estimate the angular quantity that represents
    # the predicted sentiment
    # In Russell's model, caloriesBurned is the horizontal axis (pleasrue-displeasure)
    # while beats per minute (bpm) represetns the vertical axis (sleepiness-arousal)
    
    # Parameter:
    # data_df : the data frame to be testeed upon, its columns must be two.
    # Returns
    # predicted_emotions : the textual description that displays the predicted emotion'
    
    # scale x any y to the range of -1 and 1 so that they can be applied to the AV model coordinate
    min_value_0 = min(data_df.iloc[:,0])
    max_value_0 = max(data_df.iloc[:,0])
    data_df.iloc[:,0] = data_df.iloc[:,0].apply(lambda x: preprocessing.scale(x,min_value_0, max_value_0, -1.0,1.0))
    min_value_1 = min(data_df.iloc[:,1])
    max_value_1 = max(data_df.iloc[:,1])
    data_df.iloc[:,1] = data_df.iloc[:,1].apply(lambda x: preprocessing.scale(x,min_value_1, max_value_1, -1.0,1.0))
    
    return data_df.apply(lambda x: calculate_angle(x), axis=1)
    

def get_sentiment_scores_of_AV():
    # get the terms describing the regions of the AV model and project the sentiment scores

    # Returns
    # av_chart_word_score : the dictionary whose keys are words and whose values are associated
    # sentiment scores according to AlchemyAPI
    av_chart_word_score = {}    
    
    for a_word in av_chart.values():
        response = alchemy_obj.sentiment("text", a_word)
        if (response.has_key('docSentiment')):
            if (response['docSentiment'].has_key('score')):
                sentiment_score = response['docSentiment']['score']
                if(not av_chart_word_score.has_key(a_word)):
                    av_chart_word_score[a_word] = sentiment_score
        
        # using TextBlob
        #textblob_obj = TextBlob(a_word)
        #sentiment_score = textblob_obj.sentences[0].sentiment.polarity
        #print sentiment_score
    
    return av_chart_word_score