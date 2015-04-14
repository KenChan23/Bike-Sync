import sentiment_analysis
import music_recommendation
import preprocessing
import pandas as pd

from os import listdir
from os.path import isfile, join


N_EMOTIONS = 5 
emotions = {1:"neutral", 2:"sad", 3:"happy", 4:"angry", 5:"anxious"}
#emotions_range = {(0, 0.2):1, (0.21, 0.4):2, (0.41, 0.6):3, (0.61, 0.8):4, (0.81, 1.0):5}
emotions_range = {1:(0, 0.2), 2:(0.21, 0.4), 3:(0.41, 0.6), 4:(0.61, 0.8), 5:(0.81, 1.0)}


# or maybe six emotional states
# N_EMOTIONS = 6
# emotions = {1:"neutral", 2:"sad", 3:"happy", 4:"angry"}
# emotions_range = {(0, 0.25):1, (0.26, 0.50):2, (0.51, 0.75):3, (0.76, 1.00):4}

def obtain_sentiment(ls_filenames):
    # get the data
    # here it is just the json data format
    """  TRAININING DATASET FOR """
    if (len(ls_filenames)!=0):
        data_df = pd.io.json.read_json(open(ls_filenames[0], 'r'), orient='records')
        # feature extract

        if (len(ls_filenames) >= 2):
            for i in range(1, len(ls_filenames)):
                data_df = data_df.append(pd.io.json.read_json(open(ls_filenames[i], 'r'), orient='records'), ignore_index=True)
                
        physiological_data_df = data_df.loc[:,['bpm', 'caloriesBurned']]
        
        print physiological_data_df
        
        physiological_data_df = physiological_data_df[physiological_data_df['bpm']!=0]
        
        
        pred_labels, cluster_model = sentiment_analysis.data_cluster(physiological_data_df, N_EMOTIONS)


        
        
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
    
    return pred_labels, cluster_model, physiological_data_df


def recommend_music(music_data):

    data = music_recommendation.getMusicData(music_data)

    
ls_filenames = [ join("./data/",f) for f in listdir("./data/") if isfile(join("./data/",f)) ]
ls_filenames.remove('./data/.DS_Store')

fitbit_data = ls_filenames[0:len(ls_filenames)-1]
pred_labels, k_means_obj, physiological_data_df = pd.Series(obtain_sentiment(fitbit_data))

# use this pred_labels diagram to predict the emotion at the new time series instance

recommend_music('./data/music.data')









