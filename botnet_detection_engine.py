#!/usr/bin/env python3

"""
A Flow-based Botnet Detection Engine.

As a Proof-of-Concept application of a Bio-Optimised Machine Learning Models,
to facilitate the detection of bot behaviour via their behavioural network flows.
"""

import time

from detection_engine_modules.Detector import Detector
from detection_engine_modules.cmd_line_args import get_cmd_line_args


if __name__ == "__main__":
    """
    Program entry point
    """

    # Parse command line arguments
    args = get_cmd_line_args()

    # Disable GUI is '-r'/'--read' switch is present
    # This is due to the fact that live network sniffing will not occur when reading from file
    # And thus, we disable GUI
    if args['read'] is not False:
        args['no_gui'] = False



    # TESTING
    # DELETE ME
    # DELETE ME
    # DELETE ME
    #args['no_gui'] = True



    # Sleep if a GUI instance is starting
    # Ensures adequate time is allocated for the electron instance to load
    if args['no_gui'] == True:
        time.sleep(1.5)



    # Create the detector object, passing in the command line arguments to specify operation
    detector = Detector(args)

    # Run the detector
    # Starts the Sniffer module and enters the main Detector's detection loop
    detector.run()
