#!/bin/bash

# Check number of cmd line args and limit
if [ $# -gt 5 ]
then
	show_help
	echo; echo; echo "Exceeded maximum number of command line arguments (5)"; echo;
else
	# Starts electron nodejs instance via main.js
	# Do not run GUI if -n or --no-gui switch is present
	gui=True

	for arg in "$@"
	do
		if [ "$arg" = "--no-gui" ] || [ "$arg" = "-g" ]
		then
			gui=False
			break
		fi
	done

	if [ "$gui" = True ]
	then
		npm start &
	fi

	# Executes the detection engine
	# Default (no command line arguments) sends labelled flows to electron 
	# instance for data data processing for the user
	sudo python3 botnet_detection_engine.py $@
fi
