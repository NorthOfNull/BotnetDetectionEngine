#!/bin/bash

function show_help {
	sudo python3 botnet_detection_engine.py --help
}

# Check number of cmd line args and limit
if [ $# -gt 2 ]
then
	show_help
	echo; echo; echo "Exceeded maximum number of command line arguments (2)"; echo;
else
	# Check if '--help' is requested
	if [ "$1" = "-h" ] || [ "$1" = "--help" ] || [ "$2" = "-h" ] || [ "$2" = "--help" ]
	then
		show_help
	else
		# Starts electron nodejs instance via main.js
		# Do not run GUI if -n switch is present
		if [ "$1" != "--gui" ] && [ "$2" != "--gui" ]
		then
			npm start &
		fi


		# Executes the detection engine
		# Default (no command line arguments) sends labelled flows to electron 
		# instance for data data processing for the user, without logging to a file
		sudo python3 botnet_detection_engine.py $@
	fi
fi



