# collect the heart rate data, activity level, context (?)
# context - location and speed of the user

#from NeuroPy import NeuroPy
import numpy as np
import pandas as pd
import math
import random
import sklearn as ml

import collections
import preprocessing

# data = from hardware
# we have the object-oriented design for heart rate, activity, and contxt

# heart_rate
# activity
# context

def getStdDevOfActivity(activity_one_second):
    # according to the readings, the standarad deviation value is great for clusltering and comparison
    # activity_data is a pandas object (DataFrame)
    return activity_one_second.apply(lambda a: np.std(math.abs(math.sqrt((a.X)**2 + (a.Y)**2 + (a.Z)**2))))


""" 
ACTIVITY-BASED CLASSIFICATION 

REFERENCE
    - Nirjon S, Dickerson R, Li Q, Asare P, Stankovic J, Hong D, Zhang B, Shen G, 
    Jiang X, Zhao F.  2012.  MusicalHeart: A Hearty Way of Listening to Music. 
    The 10th ACM Conference on Embedded Networked Sensor Systems (SenSys 2012)
"""

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

N_EMOTIONS = 4 
emotions = {1:"neutral", 2:"sad", 3:"happy", 4:"angry"}
emotions_heart_rate_range = {(0, 0.25):1, (0.26, 0.50):2, (0.51, 0.75):3, (0.76, 1.00):4}

# Happy, Sad, Neutral, and Angry
# according to the paper, the heart rate is in the following order
# neutral < sad < happy < angry


def heart_rate_cluster(heart_rate_df, n_emotions = N_EMOTIONS, his_current_heart_rate):
    # uses the clustering algortihm to classify the emotions using the user's heart rate
    heart_rate_df = normalize(heart_rate_df)
    k_means_obj = ml.cluster.Kmeans(n_emotions)
    k_means_obj.fit(heart_rate_df)
    
    pred_val = k_means_obj.predict(his_current_heart_rate)
    pred_emotion = ''
    # use the labeled data structures for emotions to tell you what kind of emotion the user is in
    for a_range in emotions_heart_rate_range.keys():
        if(pred_val >= a_range[0] and pred_val <= a_range[1]):
            pred_emotion = emotions[emotions_heart_rate_range[a_range]]
    
    return pred_emotion


def fitbit_data_cluster(fitbit_data_df, n_emotions, user_current_status):
    # using the data from the fitbit (activity, heart rate, blood pressure, etc)
    heart_rate_df = normalize(fitbit_data_df)
    k_means_obj = ml.cluster.Kmeans(n_emotions)
    k_means_obj.fit(fitbit_data_df)
    
    pred_val = k_means_obj.predict(user_current_status)
    pred_emotion = ''
    # use the labeled data structures for emotions to tell you what kind of emotion the user is in
    for a_range in emotions_heart_rate_range.keys():
        if(pred_val >= a_range[0] and pred_val <= a_range[1]):
            pred_emotion = emotions[emotions_heart_rate_range[a_range]]
    
    return pred_emotion


def make_recommendation(user_data, music_datatable):
    # based on the user_data, the music recommendation is being done
    
    
    
    return music_datatable[user_data]
    

"""
Using Bayesian Network to recommend music (Fuzzy Bayesian)
RERFERENCE
    - Han-Saem Park, Ji-Oh Yoo, and Sung-Bae Cho, 
    A Context-Aware Music Recommendation System Using Fuzzy Bayesian Networks with Utility Theory (2012)
"""

from skfuzzy.membership import generatemf as fuzzy

def makeFuzzyMembership(data_df, type_of_data):
    # uses the fuzzy function in order to make a fuzzy membership vector
    # depending on the type of data, the techniques are divided into two groups:
    # continuous and discrete.
    # variables such as temperature, heart rate, accelerometer, blood pressure, time are continuous
    # variables such as weather, gender, season, etc, are continuous

    # type of data is 1xn dimentional array, where n is the number of features that data_df has
    # data_df is in mxn dimensional array
    # each element in the type_of_data corresponds to the type of variable for each feature in data_df
    # : continous or discrete
    
    # Parameter
    # data_df : the data frame that contains the heart rate, gender, age, etc. all different types of data
    # type_of_data : whether the data type is cotinuous or discrete

    """ must divide the data into continous and discrete"""
    membership_vecs = []
    data_np_array = np.array(data_df)
    for i in range(len(types_of_data)):
        
        if(type_of_data[i] == 'continuous'):
            param = [0.25, 0.50, 0.75, 1.00]
            # fuzzy.trampf function returns 1-d array representing the fuzzy membershp vector
            # of a certain data
            # data_np_array[i] access the data for a particular feature (type of data)
            membership_vecs.append(fuzzy.trapmf(data_np_array[i], param))
        else:
            # if the data is discrete
            # normalize the dataset
            data_np_array[i] = preprocessing.normalize(pd.DataFrame(data_np_array[i]))
            param = [0, 0.50, 1] 
            """ YOU NEED TO CHECK THE PARAMETER AS WELL """
            membership_vecs.append(fuzzy.piecemf(data_np_array[i], param))
    
    return membership_vecs
        

def getFuzzyEvidence(membership_vecs):
    # use the membershp vectors you obtained from makeFuzzyMembership 
    # function to estimate the fuzzy evidence
    membership_vecs = pd.DataFrame(memebership_vecs)
    fuzzy_evidence = membership_vecs.apply(lambda x: sum(x), axis = 0)
    return fuzzy_evidence


def getProbForMood(membership_vecs):
    # estimate the probability that the user may be in a certain kind of mood
    fuzzy_evidence = getFuzzyEvidence(membership_vecs)    
    sum_fuzzy_evidence = fuzzy_evidence.apply(lambda x: sum(x))    
    prob = fuzzy_evidence.apply(lambda x: x/sum_fuzzy_evidence) 
    ''' YOU MUST CHECK ABOVE PROBABILITY PART '''   
    return prob


""" utility_dataset represetns a combination of attribute and state of music """


def estimate_recommendation_score_for_that_music(utility_dataset, prob):
    # make a new data table that contains the scores of user preference for a particular feature 
    # of the music and for a particular mood
    # utility_dataset is in n x m data frame, where n is the number of attributes 
    # (genre, mood, tempo, etc)
    # and m is the number of mood (it must be 4 since we are testing only four moods)
    # returns the scores of each attribute 
    attributes_type = utility_dataset.index
    mood_type = utility_dataset.columnss
    prob = np.array(prob)
    utility_dataset = np.array(utility_dataset)
    """ HERE IT IS ASSUMED THAT WE HAVE THE SAUME NUMBER OF COLUMNS (THE SAME NUMBER OF MOOD TYPE)"""
    scores = {}
    for i in range(len(utility_dataset)):
        an_attribute = utility_dataset[i]
        score = 0
        for j in range(len(a_record)):
            score = score + a_record[j]*prob[j]
        
        scores[an_attribute] = score
        
    scores = pd.DataFrame(scores)
    sums_scores = scores.apply(lambda x: sum(x))
    
    return sum_scores
    
