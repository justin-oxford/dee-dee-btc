# Dee Dee BTC
#
# A Recurrent Neural Network that learns to trade on BTC using other crypto prices
#
# This file contains:
#   create_model()  -- the function which creates the tensorflow model

#IMPORTS
# -------------------------------------------------------------------------------------------------
from imports import *

#CONSTANTS
# -------------------------------------------------------------------------------------------------


# FUNCTIONS
# -------------------------------------------------------------------------------------------------


# This function creates the RNN Model
# Inputs:
#    model_directory -- from _main Constants
#    model_name   -- from user input
#    model_steps  -- from user input
#    rnn_layers   -- from user input
#    dense_layers -- from user input
def create_model(model_directory, model_name, model_steps,
                 rnn_layers, dense_layers):
    print("# ----------> Creating Model...")
    # define model
    model = Sequential()

    # build the model based on user input
    if len(rnn_layers) > 1:
        for rnn in rnn_layers[:-1]:
            model.add(GRU(rnn, kernel_initializer='he_normal', input_shape=(model_steps, 6), return_sequences=True))
            model.add(Dropout(0.1))
            model.add(BatchNormalization())
        model.add(GRU(rnn_layers[-1], kernel_initializer='he_normal'))
        model.add(Dropout(0.1))
        model.add(BatchNormalization())
    else:
        model.add(GRU(rnn_layers[-1], kernel_initializer='he_normal'))
        model.add(Dropout(0.1))
        model.add(BatchNormalization())
    for dense in dense_layers:
        model.add(Dense(dense, activation='sigmoid', kernel_initializer='he_normal'))
        model.add(Dropout(0.1))

    # the output layer, just 2 nodes, BUY/SELL
    model.add(Dense(2))

    # compile the model
    model.compile(optimizer='adam', loss='mse', metrics=['mae', 'accuracy'])
    print(f"Model >>'{model_name}'<< Created.")
    model.summary()
    # save the model
    model.save(model_directory + model_name)
    # tf.keras.models.save_model(model, model_directory + model_name, save_format="h5")
