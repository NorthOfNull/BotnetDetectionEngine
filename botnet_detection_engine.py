 #!/usr/bin/env python3

import sys
import time
import asyncio
import argparse

from detection_engine_modules.Logger import Logger
from detection_engine_modules.Sniffer import Sniffer
from detection_engine_modules.Websocket_Controller import Websocket_Controller


#### TODO
#### EXPORT THIS TO STDIN CONTROLLER MODULE
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
    parser = argparse.ArgumentParser(usage="./run.sh [-h --help] [-n] [--log] ",
                                     description="The Botnet Detection Engine. GUI starts by default. Logging is disabled by deafult (to stdout only).")

    parser.add_argument("-n", action="store_true", help="Disables GUI.")
    parser.add_argument("--log", action="store_true", help="Log output to \"/var/log/botnet_detection_engine/detection_output.log\".")

    args = parser.parse_args()

    return args

'''
Updates the global variables depending upon the presence of the parsed
command line arguments.
'''
def update_global_vars(args):
    assert(args)

    # GUI argument check
    if(args.n):
        # Disable GUI
        print("[Cmd_Line_Args] Disabling GUI!")
        
        global GUI
        GUI = False

    if(args.log):
        # Enable logging
        print("[Cmd_Line_Args] Enabling Logging!")

        global Logging
        Logging = True



# Global Variable declarations
# Set to default values (in the case of no command line args)
GUI = True
Logging = False



# Program entry point
if __name__ == "__main__":
    # Parse command line arguments
    args = get_cmd_line_args()


    # Handle command line arguments
    update_global_vars(args)

    #print("GUI =", GUI)
    #print("Logging =", Logging)






    # Connect to GUI Backend via websocket, if the GUI variable is True
    if(GUI):
        # Websocket initialisation
        # Faciliates data transfer through a localhost socket to the backend electron nodejs server
        socket_addr = "ws://localhost:5566"

        # Create websocket connection to the nodejs websocket server
        try:
            ws_ctrl = Websocket_Controller()
            ws_ctrl.connect(socket_addr)
        except:
            print("[ Websocket ] Connection Initalisation Failed ")

            # TODO
            # EXIT PROGRAM AND CHILDREN



    # TODO
    # TODO
    # TODO
    #
    # IF LOGGING
    # WE CREATE THE LOGGER INSTANCE HERE
    # WHICH IS AN OBJECT TO HANDLE LOGGING OPERATIONS
    #
    # if(Logging):
    #   # Initialise Logging instance to handle file logging operations
    #   logger = Logger()


    # TODO
    # TODO
    # TODO
    #
    # Model Object creation
    # Model object de-serialisation of saved ML model files
    # Detector object init (which loads models)


    # Input pipeline initialisation
    # Sniffs raw data from a SPAN'd port, performs netflow feature extraction
    # TCPDUMP (pcap) | ARGUS (argus) | RA CLIENT (Formatted Neflow CSV Export)
    sniffer = Sniffer()
    sniffer.start()


    # Main processing loop
    # Loop to collect stdin input and then send it through the websocket; on full flow received
    while True:
        #flow = get_stdin_netflow()

        # Gets the flow data from the end of the sniffer's program pipeline
        # (the stdout of the last program)
        flow = sniffer.get_flows()


        # TODO
        # NETFLOW DATA GETS PREDICTED BY THE MODEL AND LABELLED HERE
        # BEFORE BEING SENT
        # flow = detector.predict(flow)


        # Output the labelled flow to stdout
        print(flow)





        # If Logging is enabled
        if(Logging):
            # Log the output to the file
            print("LOGGING LABELLED FLOW TO FILE")

            # Use Logger object to write flow to file
            # e.g.
            # logger.write(flow)


        # If GUI is running
        if(GUI):
            # Send netflow data through the websocket connection
            # If the connection fails, attempt to re-establish
            try:
                ws_ctrl.socket.send(flow)

                # TODO
                # Export the above send function to the websocket class
                # ws_ctrl.send(flow)


                # LOG TO FILE IF LOGGING IS TRUE (ENABLED)
                # LOG TO FILE IF LOGGING IS TRUE (ENABLED)
                # LOG TO FILE IF LOGGING IS TRUE (ENABLED)


                # print("SENT")
            except:
                # TODO 
                # IMPLEMENT attempt_reconnect into Websocket_Controller
                # ws_ctrl.attempt_reconnect()


                # Attempt to re-establish the Websocket connection to the server
                ws = ''
                max_attempts = 5
                print("[ Websocket_Controller ] Connection failed.")
                print("[ Websocket_Controller ] Attempting to re-establish... ")

                # TODO
                # EXPORT THIS WEBSOCKET RECONNNECTION STUFF TO THE Websocket_Controller.py MODULE


                for attempt in range(0, max_attempts):
                    try:
                        ws_ctrl.connect(socket_addr)

                        print("[ Websocket_Controller ] Connection re-established!")
                        break
                    except:
                        print("[ Websocket_Controller ] Attempt ", attempt, "failed...")
                        time.sleep(2)

                    if attempt == (max_attempts - 1):
                        print("[ Websocket_Controller ] EXCEPTION - Could not re-esablish a connection.")
                        print("--- Botnet Detection Engine Terminating ---")
                        sys.exit()
                    #
                    #    # TODO - Kill tcpdump, argus and ra processes from here!!!!
                    #
                    #    # TODO - JUST KILL PARENT PROCESS???????

        #print(netflow)
###