 #!/usr/bin/env python3

import sys
import time
import asyncio

from detection_engine_modules.Sniffer import Sniffer
from detection_engine_modules.Websocket_Controller import Websocket_Controller


# TODO
# EXPORT THIS TO STDIN CONTROLLER MODULE
def get_stdin_netflow():
    netflow = ''
    
    while not netflow.endswith('\n'):
        netflow += sys.stdin.read(1)

    return netflow[:-1]


if __name__ == "__main__":
    # Input pipeline initialisation
    # Sniffs raw data from a SPAN'd port, performs netflow feature extraction
    # TCPDUMP (pcap) | ARGUS (argus) | RA CLIENT (Formatted Neflow CSV Export)
    sniffer = Sniffer()
    sniffer.start()


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


    # Loop to collect stdin input and then send it through the websocket; on full flow received
    while True:
        #flow = get_stdin_netflow()

        flow = sniffer.get_flows()


        print(flow)

        # TODO
        # NETFLOW DATA GETS PREDICTED BY THE MODEL AND LABELLED HERE
        # BEFORE BEING SENT



        # Send netflow data through the websocket connection
        # If the connection fails, attempt to re-establish
        try:
            ws_ctrl.socket.send(flow)


            # print("SENT")
        except:
            # Attempt to re-establish the Websocket connection to the server
            ws = ''
            max_attempts = 5
            print("[ Websocket_Controller ] Connection failed.")

            # TODO
            # EXPORT THIS WEBSOCKET RECONNNECTION STUFF TO THE Websocket_Controller.py MODULE


            for attempt in range(0, max_attempts):
                print("[ Websocket_Controller ] Attempting to re-establish... ")
            
                try:
                    ws_ctrl.connect(socket_addr)

                    print("[ Websocket_Controller ] Connection re-established!")
                    break
                except:
                    print("[ Websocket_Controller ] Attempt ", attempt, "failed...")
                    time.sleep(2)

                #if ws:
                #    break
                #elif attempt == (max_attempts - 1):
                #    raise Exception("[ Websocket_Controller ] EXCEPTION - Could not re-esablish a connection")
                #
                #    # TODO - Kill tcpdump, argus and ra processes from here!!!!
                #
                #    # TODO - JUST KILL PARENT PROCESS???????

        #print(netflow)
