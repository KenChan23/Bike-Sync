""" 
preprocessing.py

this page contains the preprocessing functions of the data called from the AWS cluster
as well as the fitbit APIs. It uses pandas framework to make the data formatted for data analysis

"""

def normalize(data_df):
    # normalize the data so that it can have appropriate classes
    # data_df must be the data frame
    # if the dimenstion of data_df is nx1, tranpose it to 1xn
    if(data_df.shape[1]==1): data_df = data_df.transpose() 
    
    means = data_df.mean(axis = 1)
    std_dev= data_df.std(axis = 1)
    
    data_df = data_df.subtract(means.ix[0], axis = 'columns')
    data_df = data_df.div(std_dev.ix[0], axis= 'columns')
    
    return data_df
