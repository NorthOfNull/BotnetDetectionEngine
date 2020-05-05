'''

'''

import sys
import time
import json
import websocket


class Websocket_Client:
    '''

    '''

    def __init__(self):
        '''

        '''
        self.socket_addr = False
        self.socket = False

    '''

    '''
    def __del__(self):
        if self.socket is not False:
            self.socket.close()

        print("Deleting Websocket Client.")

    '''
    
    '''
    def connect(self, socket_addr):
        self.socket_addr = socket_addr

        try:
            self.socket = websocket.create_connection(self.socket_addr)

            print("[ Websocket_Client ] Connected to Electron!")
        except:
            self.attempt_reconnect()

        return True

    '''
    Sends the labelled_flow and alert_data as a JSON data structure through the websocket 
    '''
    def send(self, labelled_flow, alert=None):
        if alert is None:
            # Only package the labelled_flow, since we have no alerts to send
            data = {"flow": labelled_flow}
        else:
            # Package the flow and any alert json data together
            data = {"flow": labelled_flow,
                    "alert": alert}

        # Convert to json string
        data = json.dumps(data)

        # Send data
        try:
            self.socket.send(data)
        except:
            self.attempt_reconnect()
            self.socket.send(data)

        return True 

    '''

    '''
    def attempt_reconnect(self):
        '''
        Attempt to re-establish the Websocket connection to the server
        '''
        self.socket = False
        max_attempts = 5

        print("[ Websocket_Client ] Connection failed.")
        print("[ Websocket_Client ] Attempting to re-establish... ")

        for attempt in range(0, max_attempts):
            try:
                self.socket = websocket.create_connection(self.socket_addr)

                print("[ Websocket_Client ] Connection re-established!")
                break
            except:
                # Soft exception handling
                print("[ Websocket_Client ] Attempt", attempt, "failed...")
                time.sleep(2)

            if attempt == (max_attempts - 1):
                print("--- Botnet Detection Engine Terminating ---")

                # Kills the parent process (and thus, the sniffer's subprocesses,
                # as defined in the sniffer destructor)
                raise Exception("[ Websocket_Client ] ] EXCEPTION - Could not re-esablish a connection.")

        return self.socket
