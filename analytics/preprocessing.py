""" 
preprocessing.py

this page contains the preprocessing functions of the data called from the AWS cluster
as well as the fitbit APIs. It uses pandas framework to make the data formatted for data analysis

"""

class Pointer:
    # the class for pointers. This will be used to minimize the memory usage
    def __init__(self, obj): self.__obj = obj
    def get(self):    return self.__obj
    def set(self, new_obj):      self.__obj = new_obj


def normalize(data_df):
    # normalize the data frame (1d or multi-dimensional array) so that it can have appropriate classes
    # data_df must be the Data Frame or Series
    
    # Parameter : 
    # data_df : data frame (n by m dimensional array) or Series
    
    if(len(data_df.shape)==1): 
        # the data frame is series
        data_df = (data_df- data_df.mean())/data_df.std()
        data_df = data_df.transpose()
    else:
        # the data dimension is n by m dimensional array
        means = data_df.mean(axis = 1)
        std_dev= data_df.std(axis = 1)
        
        data_df = data_df.subtract(means.ix[0], axis = 'columns')
        data_df = data_df.div(std_dev.ix[0], axis= 'columns')

    return data_df



def stack_series_to_data_frame(df, series):
    # stack the series rowise to the df
    # depending on the value of n_columns, stack it columnwise
    # if the size of the column exceeds the n_columns, the deletion of the very first column must be done

    # Parameter
    # df : the old data frame
    # series : the new data frame to append rowwise (must have the same column dimension as df)
    
    # Returns
    # a new data frame (df)

    if(series.shape[0] != 0):
        # this means that the series data is arranged vertically
        # so transpose it
        series = series.transpose()
    
    if (df.shape()[1] == series.shape()[1]):
        # the COLUMN DIMENSTION MUST BE THE SAME 
        # if tthe number of the columns in the df is greater than or equal to n_columns
        df.drop('0', inplace = True)
        df = df.append(series, ignore_index = True)
    else:
        print "Failed to complete appending, because the number of columns is not matching"

    return df


def stack_data_frame_to_data_frame_columnwise(df, another_df):
    # stack the data frame to another data frame columnwise

    # Parameter :
    # df : the original data_frame
    # another_df : the new data frame (must have the same indices)

    # Returns
    # a new data frame, if the data frame is appended successfully, it will return a new data frame
    # otherwise, it will return the original one

    if (df.shape[0] == another_df.shape[0]):
        # you must make sure that they have the same number of records
        df = df.join(another_df)
    else:
        print "Failed to complete appending, because the number of records is not matching"

    return df