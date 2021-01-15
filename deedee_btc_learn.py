# Dee Dee BTC
#
# A Recurrent Neural Network that learns to trade on BTC using other crypto prices
#
# This file contains:
#    split_sequence()     -- splits the sequence into learning blocks
#    load_training_data() -- loads the data from the CSV
#    define_data_frames() -- processes the data from the CSV
#    run_training()       -- trains the model
#    main_training()      -- handler function that calls each function in turn

# IMPORTS
# -------------------------------------------------------------------------------------------------
# other dee dee files
import deedee_btc_createModel

# python modules
from imports import *

# -------------------------------------------------------------------------------------------------


# CONSTANTS
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------

# TF CONFIGURATIONS
# -------------------------------------------------------------------------------------------------
print("TF VERSION: " + str(tf.__version__))
print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))
print("\n\n")

# FUNCTIONS
# -------------------------------------------------------------------------------------------------


# split sequence into samples
def split_sequence(sequence_in, sequence_out, n_steps):
    print("Sequencing...")
    # define X (input) and y (output) as lists
    X, y = list(), list()

    # for each row/data-point
    for i in range(0, len(sequence_in)):
        # find the end of this pattern
        end_ix = i + n_steps
        # check if we are beyond the sequence
        if end_ix > len(sequence_in) - 1:
            break
        # gather input and output parts of the pattern
        # seq_x is the first 'n' rows, and seq_y is the last row which will be the output
        seq_x, seq_y = sequence_in[i:end_ix], sequence_out[end_ix]
        X.append(seq_x)
        y.append(seq_y)
    return asarray(X), asarray(y)


# Load the data
def load_training_data(address):
    # use pandas read_csv to load the data from updateData
    print("Loading data...")
    data = pd.read_csv(
        address,
        delimiter=',',
        header=0,
        index_col=None
    )
    return data


# Break the data apart into two DataFrames, on that will go into the network, and the corresponding outputs
def define_data_frames(data):
    print("Defining training/targets...")
    # define data_in as the data being fed into the model
    data_in = data[['BTC PRICE', 'BTC VOL USD',
                    'ETH PRICE', 'ETH VOL USD',
                    'LTC PRICE', 'LTC VOL USD']]
    # define data_out as the data being trained to choose
    data_out = data[["BUY", "SELL"]]
    return data_in, data_out


# runs the training process
def run_training(epochs, batch_size, data_input, data_output, model_steps, model_directory, model_name):
    # retrieve the values as floating point numbers
    values_in = data_input.values.astype('float32')
    values_out = data_output.values.astype('float32')

    # set training variables
    n_test = model_steps * 10

    # split into samples
    X, y = split_sequence(values_in, values_out, model_steps)

    # reshape into [samples, timesteps, features]
    X = X.reshape((X.shape[0], X.shape[1], 6))
    y = y.reshape((y.shape[0], 2))

    # split into train/test
    X_train, X_test, y_train, y_test = X[:-n_test], X[-n_test:], y[:-n_test], y[-n_test:]

    # define model
    model = tf.keras.models.load_model(model_directory + model_name)
    print(f"Training '{model_name}'...")
    # fit the model
    model.fit(X_train, y_train,
              epochs=epochs, batch_size=batch_size,
              verbose=1, validation_data=(X_test, y_test),
              use_multiprocessing=True, workers=8)

    # save the model
    model.save(model_directory + model_name)


def main_training(epochs, batch_size, training_data_path, model_steps, model_directory, model_name):
    raw_data = load_training_data(training_data_path)
    model_input, model_output = define_data_frames(raw_data)
    run_training(epochs, batch_size, model_input, model_output, model_steps,model_directory, model_name)
