 #!/usr/bin/env python3

import sys
import time
import asyncio

from detection_engine_modules.Websocket_Controller import Websocket_Controller

# TODO
# EXPORT THIS TO STDIN CONTROLLER MODULE
def get_stdin_netflow():
    netflow = ''
    
    while not netflow.endswith('\n'):
        netflow += sys.stdin.read(1)

    return netflow[:-1]


if __name__ == "__main__":
    socket_addr = "ws://localhost:5566"


    # Create websocket connection to the nodejs websocket server
    try:
        ws_ctrl = Websocket_Controller()
        ws_ctrl.connect(socket_addr)
    except:
        print("[ Websocket ] Connection Initalisation Failed ")

        # TODO
        # EXIT PROGRAM AND CHILDREN


    # Loop to collect stdin input and then send it through the websocket
    while True:
        netflow = get_stdin_netflow()



        # TODO
        # NETFLOW DATA GETS PREDICTED BY THE MODEL AND LABELLED HERE
        # BEFORE BEING SENT



        # Send netflow data through the websocket connection
        # If the connection fails, attempt to re-establish
        try:
            ws_ctrl.socket.send(netflow)
        except:
            # Attempt to re-establish the Websocket connection to the server
            ws = ''
            max_attempts = 5
            print("[ Websocket ] Connection failed.")



            for attempt in range(0, max_attempts):
                print("[ Websocket ] Attempting to re-establish... ")
            
                try:
                    ws_ctrl.connect()

                    print("[ Websocket ] Connection re-established!")
                except:
                    print("[ Websocket ] Attempt ", attempt, "failed...")
                    time.sleep(1)

                if ws:
                    break
                elif attempt == (max_attempts - 1):
                    raise Exception("[ Websocket ] EXCEPTION - Could not re-esablish a connection")

                    # TODO - Kill tcpdump, argus and ra processes from here!!!!

        print(netflow)
