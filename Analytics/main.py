import sentiment_analysis
import music_recommendation
import preprocessing
import pandas as pd
from os import listdir
from os import chdir
from os.path import isfile, join
from pymongo import MongoClient

N_EMOTIONS = 5 # for clustering

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


chdir("..")
fitbit_filenames = [ join("./data/fitbit/",f) for f in listdir("./data/fitbit/") if isfile(join("./data/fitbit/",f)) ]
fitbit_filenames.remove('./data/fitbit/.DS_Store')

# in the future, you will use mongoddb for connecting to the dataset
db_conn = connect("citibike")
data_frame_mongo = get_data_frame_from_mongoddb("citibike", "citibike", no_id=False)
print data_frame_mongo


""" DATA ACQUISITION """
data_df = preprocessing.get_data_df_from_JSON_Data(fitbit_filenames)
physiological_data_df = data_df.loc[:,['bpm', 'caloriesBurned']]
physiological_data_df = physiological_data_df[physiological_data_df['bpm']!=0]
print physiological_data_df['bpm'].corr(physiological_data_df['caloriesBurned'])

# it is 0.71393429575697265

#music_data = music_recommendation.getMusicData('./data/music/music.data')
#music_data.to_csv("./data/music.csv")

music_data = pd.read_csv("./data/music.csv")

# -0.245

""" SENTIMENT ANALYSIS """
pred_emotions_range, cluster_model = sentiment_analysis.data_cluster(physiological_data_df, N_EMOTIONS)
# get the last k physiological_data_df and predict the emotional state
pred_labels = cluster_model.predict(physiological_data_df.tail(music_data.shape[0]))
print pred_labels

print sentiment_analysis.predict_emotion_using_AV_model(physiological_data_df)


""" MUSIC RECOMMENDATION """
# find the predicted lables for the musics
music_data['pred_labels'] = music_recommendation.get_predicted_music_label(music_recommendation.av_chart_scores, music_data['mood_score'])
# create a data structure that contains the scores of each mood
groupd_obj = music_recommendation.create_data_structure(music_data)
 



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





