 #!/usr/bin/env python3

import sys
import argparse

from detection_engine_modules.Detector import Detector



#### TODO
#### EXPORT THIS TO STDIN CONTROLLER MODULE
######
######  OR USE FOR STDIN INPUT FOR TESTING? 
######
###def get_stdin_netflow():
###    netflow = ''
###    
###    while not netflow.endswith('\n'):
###        netflow += sys.stdin.read(1)
###
###    return netflow[:-1]



#### TODO
#### EXPORT THIS TO IT'S OWN MODULE OR CLASS??????  -----> TO cmd_line_args.py
'''
Parses the command line arguments
@returns A populated namespace object, containing the parsed arguments from sys.argv
'''
def get_cmd_line_args():
	parser = argparse.ArgumentParser(usage="./run.sh [-h --help] [--gui] [--log] ",
									 description="The Botnet Detection Engine. GUI and logging is enabled by default.")

	parser.add_argument("--gui", action="store_true", help="Disables GUI.")
	parser.add_argument("--log", action="store_true", help="Disables alert and flow logging to file.")

	args = parser.parse_args()

	return args

'''
Updates the global variables depending upon the presence of the parsed
command line arguments.
'''
def update_global_vars(args):
	global Debug

	if(args.gui == True):
		# Disable GUI        
		global GUI
		GUI = False

		if(Debug):
			print("[ Cmd_Line_Args ] Disabling GUI!")

	if(args.log == True):
		# Disable alert and flow logging
		global Logging
		Logging = False

		if(Debug):
			print("[ Cmd_Line_Args ] Disabling Logging!")

	return 0


# Global Variable declarations
# Set to default values (in the case of no command line args)
GUI = True
Logging = True

# Debugging
Debug = True


# Program entry point
if __name__ == "__main__":
	# Parse command line arguments
	args = get_cmd_line_args()

	# Handle command line arguments
	update_global_vars(args)

	# TODO
	# TODO
	# TODO
	#
	# Model Object creation
	# Model object de-serialisation of saved ML model files
	# Detector object init (which loads models)
	detector = Detector(GUI, Logging, Debug)
	detector.run()