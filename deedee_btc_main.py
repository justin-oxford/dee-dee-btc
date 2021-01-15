# Dee Dee BTC
#
# A Recurrent Neural Network that learns to trade on BTC using other crypto prices
#
# This file contains:
#   main()  -- the main function which also serves as the menu
#
# by Justin Oxford

# IMPORTS
# -------------------------------------------------------------------------------------------------
# dee dee files
import deedee_btc_updateData
import deedee_btc_learn
import deedee_btc_predict
import deedee_btc_createModel
import deedee_btc_manageModels
# -------------------------------------------------------------------------------------------------

# CONSTANTS
# -------------------------------------------------------------------------------------------------
DEEDEE_VERSION = "1.0"

# file path to where the data for training is saved
# this data should be normalized, which is done in the _updateData module
# the mirrors the PROCESSED_DATA_FILE_ADDRESS in _updateData. At some point these should be one common, variable
TRAINING_FILE_PATH = "data/btc_eth_ltc_data_normalized.csv"

# directory where the model is kept
# this is the directory plus "model_" which is them concat'd to be model_nameofmodel when you create a model
MODEL_DIRECTORY = "models/model_"

# specify the window size, how large of a window the recurrent network looks at
# step_size is dependant on intervals. if your data is BTC 1min, for example, and MODEL_STEPS = 60, the window will
# be 60 minutes.
MODEL_STEPS = 48
# -------------------------------------------------------------------------------------------------

# FUNCTIONS
# -------------------------------------------------------------------------------------------------


# Main function
# this needs to be abstracted into functions to get input, etc, for now, the menu exists here
def main():
    # run the program
    while True:
        # menu input to get the user selection, variable is a number to use in the conditionals for navigation
        user = int(input("--------> MAIN  MENU <-------- \n"
                         "[0 = close                   ]\n"
                         "[1 = get data                ]\n"
                         "[2 = create new model        ]\n"
                         "[3 = view a model            ]\n"
                         "[8 = learn                   ]\n"
                         "[9 = predict                 ]\n"
                         "[10 = predict multiple days  ]\n"
                         "\n--> "))
        # close
        if user == 0:
            break

        # process new data
        elif user == 1:
            deedee_btc_updateData.main_data_processor()

        # create a model
        elif user == 2:
            name = str(input("Model Name: "))
            print("Choose Size of Layers --->\nEnter '0' as a value to stop entering layers")
            rnn_layers = []
            while True:
                print(f"GRU Layer {len(rnn_layers)}")
                layer_size = int(input("Size -----> "))
                if layer_size == 0:
                    break
                else:
                    rnn_layers.append(layer_size)
                    continue
            dense_layers = []
            while True:
                print(f"Dense Layer {len(dense_layers)}")
                layer_size = int(input("Size -----> "))
                if layer_size == 0:
                    break
                else:
                    dense_layers.append(layer_size)
                    continue
            while True:
                print(f"You want a model with:\n"
                      f"{len(rnn_layers)} GRU Layers   -- Shaped -> {rnn_layers}\n"
                      f"{len(rnn_layers)} Dense Layers -- Shaped -> {dense_layers}\n"
                      f"Correct? (yes/no)")
                confirmation = str(input("---> "))
                if confirmation == "yes":
                    deedee_btc_createModel.create_model(MODEL_DIRECTORY, name, MODEL_STEPS,
                                                        rnn_layers, dense_layers)
                    break
                elif confirmation == "no":
                    print("!--> Model creation cancelled!")
                    break
                else:
                    print("You must choose 'yes' or 'no'\n")

        # show a model's info
        elif user == 3:
            deedee_btc_manageModels.main_manage_models(MODEL_DIRECTORY)

        # train a model
        elif user == 8:
            name = str(input("Enter Model Name To Train ---> "))
            epochs = int(input("Number of Epochs --> "))
            batch_size = int(input("Batch Size (recommend 128,256+) --> "))
            deedee_btc_learn.main_training(
                epochs,
                batch_size,
                TRAINING_FILE_PATH,
                MODEL_STEPS,
                MODEL_DIRECTORY,
                name)

        # use a model to make prediction
        elif user == 9:
            model = str(input("Name of Model --> "))
            predict_row = int(input("Prediction Row [0 = most recent] --> "))
            prediction = deedee_btc_predict.main_prediction(
                TRAINING_FILE_PATH,
                MODEL_DIRECTORY,
                model,
                MODEL_STEPS,
                predict_row)
            print(f"\n\n## --> BTC Next Hour:\n\n"
                  f"Buy:  {round(prediction[0][0] * 100.0, 1)}%\n"
                  f"Sell: {round(prediction[0][1]* 100.0, 1)}%\n\n\n\n\n")

        # use a model to make a chain of predictions
        elif user == 10:
            model = str(input("Name of Model --> "))
            predict_row = int(input("Prediction Row [0 = most recent] --> "))
            number_of_hours = int(input("Number of Hours --> "))
            for i in range(number_of_hours):
                prediction = deedee_btc_predict.main_prediction(
                    TRAINING_FILE_PATH,
                    MODEL_DIRECTORY,
                    model,
                    MODEL_STEPS,
                    predict_row + i)
                print(f"\n\n## --> BTC Hour {i}:\n\n"
                      f"Buy:  {round(prediction[0][0] * 100.0, 1)}%\n"
                      f"Sell: {round(prediction[0][1]* 100.0, 1)}%\n\n\n\n\n")

        # tell the user they didn't input a valid choice
        else:
            print("Selection Invalid")


# Call main to start the program
main()
