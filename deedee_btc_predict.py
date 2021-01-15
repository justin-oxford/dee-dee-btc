# Needs Documentation
#
#
#
#

# IMPORTS
# -------------------------------------------------------------------------------------------------
# python modules
from imports import *

# -------------------------------------------------------------------------------------------------

# CONSTANTS
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------

# FUNCTIONS
# -------------------------------------------------------------------------------------------------


# Load the data
# this is the same as the other function and should be put in it's own file of resources
def load_training_data(address):
    # use pandas read_csv to load the data from updateData
    data = pd.read_csv(
        address,
        delimiter=',',
        header=0,
        index_col=None
    )
    return data


# Defines the range from the data to make a prediction
# Takes in 3 values:
# ---- [data]           The raw data with all 25,000+ rows
# ---- [model_steps]    The steps (window of data to look at)
# ---- [prediction_row] Where to take the data from in the rows. Row 0 means taking the most recent data.
# It returns the data, model_steps long to be predicted
def set_prediction_range(data, model_steps, prediction_row):
    # define data_cols as the data being fed into the model
    data_cols = data[['BTC PRICE', 'BTC VOL USD',
                      'ETH PRICE', 'ETH VOL USD',
                      'LTC PRICE', 'LTC VOL USD']]
    # cull the list to be model_steps rows, between prediction_row and pred_row + model_steps
    data_culled = data_cols[prediction_row:prediction_row + model_steps]
    values_in = data_culled.values.astype('float32')
    values_in = values_in.reshape((1, values_in.shape[0], values_in.shape[1]))
    return values_in


# Makes the prediction based off of the data and the tf model
# Takes in 2 values:
# ---- [model_name]  The name of the model to get the saved trained model
# ---- [data]        The data to predict off of
# It returns the prediction [0 = no result, 1 = buy, 2 = sell]
def make_prediction(model_directory, model_name, data):
    prediction = [[0.0, 0.0]]
    try:
        model = tf.keras.models.load_model(
            model_directory + model_name,
            custom_objects=None,
            compile=True)
        prediction = model.predict(data)
    except Exception as err:
        print("Unable to make prediction")
        print(err)
    return prediction


# The main function for prediction
def main_prediction(data_address, model_directory, model_name, model_steps, prediction_row):
    raw_data = load_training_data(data_address)
    predict_data = set_prediction_range(raw_data, model_steps, prediction_row)
    prediction = make_prediction(model_directory, model_name, predict_data)
    return prediction
