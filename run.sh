#!/bin/bash

# Starts electron nodejs instance via main.js

# IF -n CMD LINE ARGUMENT 
# WE DONT RUN NMP START
#npm start &


# Executes the detection engine
# Sends labelled flows to electron instance for data data processing for the user

sudo python3 botnet_detection_engine.py   # INSERT CMD LINE ARG LIST DIRECTLY INTO THIS BASH STATEMENT
e