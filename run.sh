#!/bin/bash

# Check number of cmd line args and limit
if [ $# -gt 5 ]
then
	python3 botnet_detection_engine.py --help
	echo; echo; echo "Exceeded maximum number of command line arguments (5)"; echo;
else
	# Starts electron nodejs instance via main.js
	# Do not run GUI if -n or --no-gui switch is present
	# Also does not run if reading from a inputted .pcap or network flow file
	gui=True

	for arg in "$@"
	do
		if [ "$arg" = "--no-gui" ] || [ "$arg" = "-g" ] || [ "$arg" = "--read" ] || [ "$arg" = "-r" ]
		then
			gui=False
			break
		fi
	done

	if [ "$gui" = True ]
	then
		# If gui is enabled and files are not being read instead of sniffing from the network
		# Start the user interface instance
		npm start &
	fi

	# Executes the detection engine
	# Default (no command line arguments) sends labelled flows to electron 
	# instance for data data processing for the user
	sudo python3 botnet_detection_engine.py $@
fi
