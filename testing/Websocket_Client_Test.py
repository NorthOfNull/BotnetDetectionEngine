import unittest

import time
import os, signal, subprocess

from detection_engine_modules.Websocket_Client import Websocket_Client

#
# Websocket_Client module testing file.
#

# Black box testing
class bb_ClientTest(unittest.TestCase):
    # __init__
    def test_init(self):
        '''
        Testing init funciton returns an object.
        Input - Not required
        Requires - Nothing
        Expected output - A Websocket_Client object
        '''
        websocket_client = False
        websocket_client = Websocket_Client()

        self.assertTrue(websocket_client)


    # connect
    def test_connect__no_arg(self):
        '''
        Testing the connect function's return value, without an argument.
        Input - Nothing
        Requires - A Websocket_Client object.
        Expected output - Exception
        '''
        websocket_client = Websocket_Client()

        self.assertRaises(Exception, websocket_client.connect)

    def test_connect__with_invalid_arg(self):
        '''
        Testing the connect function's return value, with an invalid address string.
        Input - An invalid address string.
        Requires - A Websocket_Client object.
        Expected output - Exception.
        '''
        websocket_client = Websocket_Client()

        invalid_addr = "not_an_address"

        self.assertRaises(Exception, websocket_client.connect, invalid_addr)


    # send
    def test_send__no_arg(self):
        '''
        Testing the send function's return value, without the required positional arguments.
        Input - Nothing
        Requires - A Websocket_Client object.
        Expected output - TypeError exception.
        '''
        websocket_client = Websocket_Client()

        self.assertRaises(TypeError, websocket_client.send)





# White box testing
class wb_ClientTest(unittest.TestCase):
    # __init__
    def test(self):
        '''
        Testing the values stored in the initialised object.
        Input - Nothing
        Requires - Nothing
        Expected output - 
        '''
        websocket_client = Websocket_Client()

        self.assertFalse(websocket_client.socket_addr)
        self.assertFalse(websocket_client.socket)
