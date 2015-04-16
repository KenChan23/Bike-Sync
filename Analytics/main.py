import sentiment_analysis
import music_recommendation
import preprocessing
import pandas as pd
from os import listdir
from os import chdir
from os import getcwd
from os.path import isfile, join
from pymongo import MongoClient

N_EMOTIONS = 5 
emotions = {1:"neutral", 2:"sad", 3:"happy", 4:"angry", 5:"anxious"}


HOSTNAME = "ec2-54-172-195-184.compute-1.amazonaws.com"
DATABASE = "citibike"
USERNAME = "kenchan"
PASSWORD = "root"

def connect(dbname):
    # Substitute the 5 pieces of information you got when creating
    # the Mongo DB Database (underlined in red in the screenshots)
    # Obviously, do not store your password as plaintext in practice
    
    connection = MongoClient("ds062097.mongolab.com",62097)
    db_conn= connection[dbname]
    db_conn.authenticate("root","root")
    return db_conn


def get_data_frame_from_mongoddb(dbname, collection_name, query={}, no_id=True):

    # Connect to MongoDB
    db_conn = connect(dbname)

    # Make a query to the specific DB and Collection
    cursor = db_conn[collection_name].find(query)

    # Expand the cursor and construct the DataFrame
    df =  pd.DataFrame(list(cursor))

    # Delete the _id
    if no_id:
        del df['_id']

    return df


def obtain_sentiment(physiological_data_df):
    # using the data from the fitbit, predict the sentiment of the user
    # Parameter
    # physiological_data_df : data frame that will be used for 
    # Returns
    # pred_emotions_range : the predicted range of emotions 
    # cluster_model : the predicition model

    
    physiological_data_df = physiological_data_df[physiological_data_df['bpm']!=0]
    
    # get the predicted emotions range as well as the actual clustering model
    pred_emotions_range, cluster_model = sentiment_analysis.data_cluster(physiological_data_df, N_EMOTIONS)

    # pred_labels = pred_labels.apply(lambda x: sentiment_analysis.determine_emotion(x, emotions_range))
    
    #print pred_labels
    # put this into the list of containers pointing to the data frame itself
    # DATA MUST HVE THE COLUMNS LABELS
    """
    acceleration_data_df = Pointer(feature_extract_acceleration(acceleration_data_df))
    enviro_data_df = Pointer(feature_extract_environment(enviro_data_df))
    signl_data_df = Pointer(feature_extract_singal_data(signal_data_df))
    
    n_data = 3 # for now
    
    data_ls.append(acceleration_data_df)
    data_ls.append(enviro_data_df)
    data_ls.append(enviro_data_df)
    
    # stack the data frame to be run for 
    for i in range(0, n_data)
    	data_df = preprocessing.stack_data_frame_to_data_frame_columnwise(data_df, data_ls[i].get())
    """ 
    
    """
    # cross-validation of the data
    data_train, data_test = ml.cross_validation.train_test_split(data_df, test_size = 0.4)
    # cluster the data to show the predicted labes for the emotions and 
    # put this into classification learning model
    pred_labels = sentiment_analysis.data_cluster(data_train, N_EMOTIONS, emotions_range)
    learning_model = sentiment_analysis.learning(data_train, pred_lables)
    # predict the sentiment
    pred_sentiment = learning_model.predict(data_test)
    """
    
    return  pred_emotions_range, cluster_model


def recommend_music(music_data):

    data = music_recommendation.getMusicData(music_data)
    
    return data


chdir("..")
fitbit_filenames = [ join("./data/fitbit/",f) for f in listdir("./data/fitbit/") if isfile(join("./data/fitbit/",f)) ]
fitbit_filenames.remove('./data/fitbit/.DS_Store')

# in the future, you will use mongoddb for connecting to the dataset
db_conn = connect("citibike")

data_frame_mongo = get_data_frame_from_mongoddb("citibike", "citibike", no_id=False)
print data_frame_mongo

data_df = preprocessing.get_data_df_from_JSON_Data(fitbit_filenames)
pred_emotions_range, cluster_model = pd.Series(obtain_sentiment(data_df.loc[:,['bpm', 'caloriesBurned']]))

# get the most k recent time frame of your fitbit data



# use this pred_labels diagram to predict the emotion at the new time series instance
music_data = recommend_music('./data/music/music.data')




# intelligence 
# coginitive mimic
# symbolic AI vs. Neural Nets
# Reasoning vs. Perception (or knowledge)

# brain in a vet vs. adapted AI
# narrow vs wide AI

# AI begins in 1943. 
# McCulloch + Pitts --> 
# Alan Turing (Turing Machine) --> in 1950, publishes Turing Test for testing intelligence of a machine

# Dartmouth Workshop 1956





