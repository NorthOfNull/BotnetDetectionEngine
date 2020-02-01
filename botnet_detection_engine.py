 #!/usr/bin/env python3

import sys
import time
import asyncio
import websocket

def get_stdin_netflow():
    netflow = ''
    
    while not netflow.endswith('\n'):
        netflow += sys.stdin.read(1)

    return netflow[:-1]


if __name__ == "__main__":
    socket = "ws://localhost:5566"

    # Create websocket connection
    try:
        ws = websocket.create_connection(socket)
    except:
        ws = False
        print("[ Websocket ] Connection Initalisation Failed ")


    # Loop to collect stdin input and then send it through the websocket
    while True:
        netflow = get_stdin_netflow()

        # Send netflow data through the websocket connection
        # If the connection fails, attempt to re-establish
        try:
            ws.send(netflow)
        except:
            # Attempt to re-establish the Websocket connection to the server
            ws = ''
            attempts = 5
            print("[ Websocket ] Connection failed.")

            for attempt in range(0, attempts):
                print("[ Websocket ] Attempting to re-establish... ")
            
                try:
                    ws = websocket.create_connection(socket)

                    print("[ Websocket ] Connection re-established!")
                except:
                    print("[ Websocket ] Attempt ", attempt, "failed...")
                    time.sleep(1)

                if ws:
                    break
                elif attempt == (attempts - 1):
                    raise Exception("[ Websocket ] EXCEPTION - Could not re-esablish a connection")

                    # TODO - Kill tcpdump, argus and ra processes from here!!!!

        print(netflow)
