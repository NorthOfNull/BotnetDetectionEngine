 #!/usr/bin/env python3

import sys
import argparse

from detection_engine_modules.Detector import Detector


#### TODO
#### EXPORT THIS TO IT'S OWN MODULE OR CLASS??????  -----> TO cmd_line_args.py
'''
Parses the command line arguments
@returns A populated namespace object, containing the parsed arguments from sys.argv
'''
def get_cmd_line_args():
	parser = argparse.ArgumentParser(description="The Botnet Detection Engine. GUI and logging is enabled by default.")

	parser.add_argument("-g", "--gui", action="store_false", help="Disables GUI.", default=True)
	parser.add_argument("-l", "--log", action="store_false", help="Disables alert and flow logging to file.", default=True)
	parser.add_argument("-d", "--debug", action="store_true", help="Enable verbose debugging output.", default=False)
	parser.add_argument("-r", "--read", action="store", help="Read from \'.pcap\' or Network Flow file.", default=False)

	args = parser.parse_args()

	return args


# Program entry point
if __name__ == "__main__":
	# Parse command line arguments
	args = get_cmd_line_args()

	print(args)

	# Handle command line arguments
	#update_global_vars(args)

	# TODO
	# TODO
	# TODO
	#
	# Model Object creation
	# Model object de-serialisation of saved ML model files
	# Detector object init (which loads models)
	detector = Detector(args)
	detector.run()