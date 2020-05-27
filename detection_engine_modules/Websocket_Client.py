"""
The Websocket_Client Module.
"""

import sys
import time
import json
import websocket


class Websocket_Client:
    """
    The Websocket Client class controls the connection and data transfer to the Websocket Server.

    This class will attempt to reconnect the instance to the server in the case of a failed data send attempt.

    If reconnect fails, an exception is raised.
    """

    def __init__(self):
        """
        The constructor of the Websocket_Client object.

        Attributes:
            socket_addr (string): The address of the websocket server.
            socket (False or :obj:'WebSocket'): The websocket's connection socket storage variable.
        """
        self.socket_addr = False
        self.socket = False

    def __del__(self):
        """
        The Websocket_Client object's destructor.

        Explicitally closes a running socket.
        """
        if self.socket is not False:
            self.socket.close()

        print("Deleting Websocket Client.")

    def connect(self, socket_addr):
        """
        This function attempt to create a conneciton to a websocket server.

        If a connection cannot be created, it also attempts the reconnect functionality.

        Args:
            socket_addr (string): An address of the websocket server that it intends to attempt a connection with.

        Returns:
            (bool): True if it successfully creates a connection.
        """
        self.socket_addr = socket_addr

        try:
            self.socket = websocket.create_connection(self.socket_addr)
        except:
            self.attempt_reconnect()
            
        print("[ Websocket_Client ] Connected to Electron!")

        return True

    def send(self, labelled_flow, alert=None):
        """
        Attempts to send the labelled_flow and alert_data as a JSON data structure through the active websocket connection.

        Attempts to reconnect if the data send via the socket fails.

        Args:
            labelled_flow (string): The labelled flow data string.
            alert (None or json-formatted string): The alert data, if required to be sent.

        Returns:
            (bool): True, if the data is sent successfully.
        """
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


    def attempt_reconnect(self):
        """
        Attempts to re-establish the Websocket connection to the server.

        Makes a maximum of 5 reconnect attempts. If reconnect is successful, the function returns a new socket connnection object; 
        else, an exception is raised.

        Returns:
            socket (:obj:'WebSocket'): The WebSocket's connection object, in the case of a successful reconnect attempt. 
        """
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
