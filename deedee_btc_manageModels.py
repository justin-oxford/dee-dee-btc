# Dee Dee BTC
#
# A Recurrent Neural Network that learns to trade on BTC using other crypto prices
#
# This file contains:
#   describe_model()      -- displays a summary of the desired model
#   main_manage_models()  -- this function contains the menu and navigation logic for model management

#IMPORTS
# -------------------------------------------------------------------------------------------------
from imports import *

#CONSTANTS
# -------------------------------------------------------------------------------------------------


# FUNCTIONS
# -------------------------------------------------------------------------------------------------


# displays a summary of the desired model
def describe_model(model_directory, model_name):
    print(f"---> Loading Model : '{model_name}'")
    model = tf.keras.models.load_model(model_directory + model_name)
    print(f"---> Summary of '{model_name}'")
    model.summary()


# this function contains the menu and navigation logic for model management
def main_manage_models(model_dir):
    while True:
        print("------> Saved Models <------\n")

        # get all of the model names
        model_list = os.listdir('models')
        # This prints all the names so you can type what you want
        for model in model_list:
            print(f"# {model[6:]}")
        chosen_model = str(input("Which model would you like to manage?\n---> "))
        describe_model(model_dir, chosen_model)
        choice = int(input("\n[0 - return to main menu] [1 - manage another model]\n\n---> "))
        if choice == 0:
            break
        elif choice == 1:
            continue
        else:
            print(f"{choice} is not a valid input")
