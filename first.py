# collect the heart rate data, activity level, context (?)
# context - location and speed of the user

#from NeuroPy import NeuroPy
import numpy as np
import pandas as pd
import math
import random
import sklearn as ml
import collections

# data = from hardware
# we have the object-oriented design for heart rate, activity, and contxt

# heart_rate
# activity
# context

# Happy, Sad, Neutral, and Angry
# according to the paper, the heart rate is in the following order
# neutral < sad < happy < angry

N_EMOTIONS = 4 
emotions = {1:"neutral", 2:"sad", 3:"happy", 4:"angry"}
emotions_heart_rate_range = {(0, 0.25):1, (0.26, 0.50):2, (0.51, 0.75):3, (0.76, 1.00):4}

def getStdDevOfActivity(activity_one_second):
    # according to the readings, the standarad deviation value is great for clusltering and comparison
    # activity_data is a pandas object (DataFrame)
    return activity_one_second.apply(lambda a: np.std(math.abs(math.sqrt((a.X)**2 + (a.Y)**2 + (a.Z)**2))))


def stackSeriesToDataFrame(df, series, n_columns):
    # stack the series columwise to the df
    # depending on the value of n_columns, stack it columnwise
    # if the size of the column exceeds the n_columns, the deletion of the very first column must be done
    
    if(df.shape()[1]>=n_columns):
        # if tthe number of the columns in the df is better than n_columns
        df.drop('0', inplace = True)
        
    df = df.append(series)
    
    return df

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

def normalize(data_df):
    # normalize the data so that it can have appropriate classes
    # averages and standard deviations must be the 
    means = data_df.mean(axis = 1)
    std_dev= data_df.std(axis = 1)
    
    data_df = data_df.substract(means.ix[0], axis = 'columns')
    data_df = data_df.div(std_dev.ix[0], axis= 'columns')
    
    return data_df
    

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


def make_recommendation(user_data, music_datatable):
    # based on the user_data, the music recommendation is being done
    
    
    
    return music_datatable[user_data]
    


    
    
    
    


    