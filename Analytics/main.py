import sentiment_analysis
import music_recommendation
import preprocessing
import pandas as pd
from os import listdir
from os import chdir
from os import system
from time import sleep

from os.path import isfile, join
from pymongo import MongoClient

N_EMOTIONS = 5 # for clustering

HOSTNAME = "ec2-54-172-195-184.compute-1.amazonaws.com"
DATABASE = "citibike"
USERNAME = "kenchan"
PASSWORD = "root"
PORT = 21017

def connect(dbname):
    # Substitute the 5 pieces of information you got when creating
    # the Mongo DB Database (underlined in red in the screenshots)
    # Obviously, do not store your password as plaintext in practice
    
    connection = MongoClient(HOSTNAME,PORT)
    db_conn= connection[DATABASE]
    db_conn.authenticate(USERNAME,PASSWORD)
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


chdir("..")
fitbit_filenames = [ join("./data/fitbit/",f) for f in listdir("./data/fitbit/") if isfile(join("./data/fitbit/",f)) ]
fitbit_filenames.remove('./data/fitbit/.DS_Store')

# in the future, you will use mongoddb for connecting to the dataset
#db_conn = connect("citibike")
#data_frame_mongo = get_data_frame_from_mongoddb("citibike", "citibike", no_id=False)
#print data_frame_mongo




# -0.245
i = 0

while (True):
    
    """ UPDATE THE FITBIT / MUSIC DATA """
    chdir("./write_data/")
    system("fitbit.py")
    chdir("..")
    # as an alternative, you set up the connection to mongodb in aws instance
    
    """ DATA ACQUISITION """
    data_df = preprocessing.get_data_df_from_JSON_Data(fitbit_filenames)
    physiological_data_df = data_df.loc[:,['bpm', 'caloriesBurned']]
    physiological_data_df = physiological_data_df[physiological_data_df['bpm']!=0]
    print physiological_data_df['bpm'].corr(physiological_data_df['caloriesBurned'])
    
    # it is 0.71393429575697265
    
    #music_data = music_recommendation.getMusicData('./data/music/music.data')
    #music_data.to_csv("./data/music.csv")
    
    music_data = pd.read_csv("./data/music.csv")    
    
    
    """ SENTIMENT ANALYSIS """
    pred_emotions_range, cluster_model = sentiment_analysis.data_cluster(physiological_data_df, N_EMOTIONS)
    # get the last k physiological_data_df and predict the emotional state
    pred_labels = cluster_model.predict(physiological_data_df.tail(music_data.shape[0]))
    
    pred_angles_using_AV =  sentiment_analysis.predict_emotion_using_AV_model(physiological_data_df)
    pred_labels_using_AV = pred_angles_using_AV.apply(lambda x: sentiment_analysis.get_predicted_labels_using_angles(x))
    pred_labels_using_AV = pred_labels_using_AV[pred_labels_using_AV != -1]
    
    """ MUSIC RECOMMENDATION """
    # find the predicted lables for the musics
    music_data['pred_labels'] = music_recommendation.get_predicted_music_label(music_recommendation.av_chart_scores, music_data['mood_score'])
    # create a data structure that contains the scores of each mood
    groupd_obj = music_recommendation.create_data_structure(music_data)
    
    # use the data (predicted labels of the emotion and the categorization of the musics)
    # to recommenda the music
    recommended_songs_label = music_recommendation.map_from_emotion_to_music_label(pred_labels_using_AV.tail(40), groupd_obj)
    music_recommendation.get_songs_from_label(recommended_songs_label, groupd_obj, music_data)
    
    sleep(60)

    i = i + 1
    
    print str(i) + " minutes have passed "
    
 


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





