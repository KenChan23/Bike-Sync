"""
    sentiment_analysis.py

"""


# collect the heart rate data, activity level, context (?)
# context - location and speed of the user


import numpy as np
import pandas as pd
import math
import random
import sklearn as ml
import sklearn.cluster as clustering
from graphlab import kmeans
from graphlab import SFrame
import scipy.fftpack as fft # this is Fast Fourier Transform
import collections
import preprocessing
import time

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

# Happy, Sad, Neutral, and Angry
# according to the paper, the heart rate is in the following order
# neutral < sad < happy < angry



def determine_emotion(one_record, emotions_range):
    # using the preb_labels's data, predict the emotion
    for a_range in emotions_range.keys():
        if(one_record >= a_range[0] and one_record <= a_range[1]):
            pred_emotion = emotions_range[a_range]
    
    return pred_emotion


def data_cluster(data_df, n_emotions, emotions_range):
    # using the data_df, it clusters into the group of emotions indicated by n_emotions
    # and using the new data that is coming, it gives you the predicted labels 
    # and return the data frame as well as the label in it

    """ MAY RUN SOME CROSS-VALIDATION ALGORITHM"""

    data_df = preprocessing.normalize(data_df)
    #data_sf = SFrame(data_df) # turn this into SFrame
    #k_means_obj = kmeans.create(data_sf, num_clusters = n_emotions)
    
    k_means_obj = clustering.KMeans(n_emotions)
    k_means_obj.fit(data_df)
    pred_labels = pd.DataFrame(k_means_obj.predict(data_df))
    
    return pred_labels, k_means_obj

def tell_emotions(actual_sentiment):
    # use the hash table structure whose key is the score of the sentiment and whose value is the textual description
    # of the sentiment
    return 0


def create_an_emotional_model(pred_sentiments_df):
    # given the predicted sentiment, create for each instance the emotional model that
    # contains the scores of Arousal-Valence model

    def get_AV_score(sentiment_score):
        # as we know, the number of emotions we are currently using are five
        # N_EMOTIONS = 5 
        # emotions = {1:"neutral", 2:"sad", 3:"happy", 4:"angry", 5:"anxious"}
        # emotions_range = {(0, 0.2):1, (0.21, 0.4):2, (0.41, 0.6):3, (0.61, 0.8):4, (0.81, 1.0):5}
        return 0
    
    return 0
    
        
    

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
    for i in range(len(type_of_data)):
        
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
    membership_vecs = pd.DataFrame(membership_vecs)
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



"""
Using HAR Problem Techniques
RERFERENCE
    - Oscar D. Lara and Miguel A. Labrador, 
    A Survey on Human Activity Recognition using Wearable Sensors(2013)
"""

""" IMPORTANT! 
    
    the data format for this technique

            attribute 1  |  attribute 2  |  attribute 3  |  attribute 4     ... | Sentiment
    =========================================================================== |===========
                                                                                |
    time 1                                                                      |
                                                                                |
    =========================================================================== |
                                                                                |        
    time 2                                                                      |
                                                                                |
    =========================================================================== |
                                                                                |
    time 3                                                                      |
                                                                                |
    =========================================================================== |
                                                                                |
    time 4                                                                      |  
                                                                                |
    =========================================================================== |
    ...                                                                         |

    index : time series (time frame)
    columns : attributes (acceleration, signal, environement data)

    
"""


"""GET THE DATA"""
""" use the fitbit API and other data sources to format the data """
def get_acceleration_data(acceleration_data_raw): return 0 # use the fitbit's activity tracker data
    # Returns 
    # the data frame of acceleration whose features are x,y, and z of the data
def get_physiological_data(signal_data_raw): return 0 # heart rate, pualse, rate, blood pressure
def get_environmental_data(environment_data_raw): return 0 # the environmental data includes traffic, weather, citibike historical data

"""FEATURE EXTRACTION PART"""

# time window assignment
def collect_data_based_on_time_window(df, time_window=30):
    # based on the value of time_window, collect the dataset such that you have the time-windowed dataset
    # dividing the measured raw data into time window chunks is more efficient

    # Parameter
    # df : the old data frame
    # time_window : the time interval after which the new data instance is being collected

    # Returns
    # the new data frame that has the new data

    """ need the fitbit device to implement this and see how they are doing it"""
    # the approach
    # once the certain time has passed, collect the data and stack to the data frame
    prevTime = time.clock()
    while True:
        """ let fitbit collect the data for now --> FIGURE OUT HOW TO IMPLEMENT THIS"""
        currTime = time.clock()
        if(currTime - prevTime >= time_window):
            # this is the place  to collect the new dataset 
            # collect the new real-time data
            new_data = get_new_data()
            # stack the new data
            df = preprocessing.stack_series_to_data_frame(df, new_data)

    return df 
    """ NEED TO THINK ABOUT THIS PART CAREFULLY, as it doesn't get out of the loop """


# acceleration
def feature_extract_acceleration(acceleration_data_df, method = 'PCA'):
    # conducts the feature extraction of the acceleration data
    # according to the paper, it employs many difference techniques, including the Principal Component Analysis (PCA)
    # or Discrete Cosine Transform (DCT)

    # Parameter
    # acceleration_data_df : the data frame that contains the acceleration data (a_x, a_y, a_z)
    # method : the method for feature extraction. There are several techniques employed in this paper. 
    # Depending on the method parameter, one can choose to use 

    # Returns 
    # the transformed data

    if (method == 'PCA'):
        # 1. Principal component analysis
        a_PCA = ml.decomposition.PCA(1) # the number of components to extract may change
        a_PCA.fit(acceleration_data_df)
        transformed_data = a_PCA.predict(acceleration_data_df)
    elif (method == 'DCT'):
        # 2. Dicsrete Consine Transform
        transformed_data = pd.DataFrame(fft.dct(np.array(acceleration_data_df)))

    return transformed_data


# environment
def feature_extract_environment(environemtnal_data_df):
    # the feature extraction method for environment variables
    # the environment variables include temperature, humidity, light, altitude, Citibike APIs

    # IMPORTANT
    # when implementing citibike APIs, you must extract the data such that it will be in the same format as
    # the data frame you are using (time window is the record)

    # may have to write some MapReduce code to process the Citibike data...

    # Parameter
    # environmental_data_df : the data frame for the environment
    """ 
    IMPORTANT
    the features
    temperature, 
    humidity, 
    # of bike travels based upon gender, 
    # of bike travels based upon age,
    # of bike travels based upon geospatical location of where he is on that time frame,
    # of bike travels based upon season

    """               

    # Returns
    # the transformed environmental data frame

    # transform the dataset based upon the type of attributes
    # e.g. temperature --> time domain
    # e.g. 


    return transformed_data


# vital signal
def feature_extract_singal_data(signal_data_df):
    # according to the paper described, it extracts the features as follows:
    # get the signal from signal_data_df, and feature-extract using the structural detector technique
    # the signal data includes heart rate, blood pressure, etc.

    # Parameter
    # signal_data_df : multi-dimensional series or array that includes but not limited to heart rate and blood pressure
    # the data can be expanded depending on how many kinds of singal data we can get

    # Returns
    # the transformed value of the signal data frame

    # choose the structural detectors
    # there are many differenct functions to become the structural detector (linear, polynomial, etc),
    # in this case, we use the simple ordinary least square linear regression function 
    # F(t) = sigma(w*t) + b
    
    # First, normalize the data for each attribute
    normalized_data = preprocessing.normalize(signal_data_df)

    # create two new classes : the function for the raw data and the function for the flipped data
    linear_obj_raw = ml.linear_model.LinearRegression()
    
    # fit the data
    linear_obj_raw.fit(normalized_data)

    return linear_obj_raw.predict(normalized_data)



""" LEARNING """
# in this part, you can use any supervising learning algorithms to train the model using the feature-extracted dataset
# and to predict what kind of sentiment this person is in
# the strategy
# given the context of our current sytem, we have to use the unsupervised learning system to
# cluster into groups of senitment status
# then, the classified data are analyzed into classification algorithms
# examples : decision trees, support vector machines, Naive Bayes, 

# data_df and pred_labels are from the 
def learning(data_df, pred_labels):
    # the function that allows the use of many supervised learning algorithms
    # Parameter
    # data_df : the data frame to test upon, it must have the dataset 
    # pred_labels : the labels you get from the unsupervised learning algorithm (clustering)
    
    # Return
    # return the best learning model

    # Random Forest (decision tree)
    # Uses the randome forest regression
    random_forest = ml.ensemble.RandomForestRegressor(n_estimators = 15)
    random_forest.fit(data_df, pred_labels)

    # Support Vecotr Machine 
    svm = ml.svm.LinearSVR(loss='l2')
    svm.fit(data_df, pred_labels)

    # compare errors, and return the model with minimal error
    if(random_forest.score(data_df) > svm.score(data_df)):
        return random_forest
    else:
        return svm




    
