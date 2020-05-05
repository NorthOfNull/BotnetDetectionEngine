import unittest

import os, time, signal, subprocess

from detection_engine_modules.cmd_line_args import get_cmd_line_args
from detection_engine_modules.Detector import Detector

#
# Detector module testing file.
#

# Black box testing
class bb_DetectorTest(unittest.TestCase):
    # __init__
    def test_init(self):
        '''
        Testing default behaviour of the Detector's constructor.
        Input - Default return values of a get_cmd_line_args function call.
        Requires - Websocket server to be running.
        Expected output - Detector object is successfully instantiated.
        '''
        args = get_cmd_line_args()

        sp = subprocess.Popen("npm start", shell=True, preexec_fn=os.setsid)

        detector = False
        detector = Detector(args)

        self.assertTrue(detector)

        detector.ws_client.socket.close()

        os.killpg(sp.pid, signal.SIGTERM)
        time.sleep(3)


# White box testing
class wb_DetectorTest(unittest.TestCase):
    # __init__
    def test_init__with_inverted_default_arg_bool_values(self):
        '''
        Testing behaviour of the Detector's constructor with inverted values in the args argument.
        Input - Dictionary of values simulating non-default output get_cmd_line_args function call.
        Requires - Nothing
        Expected output - Detector object is successfully instantiated.
        '''
        args = {'no_gui':False,
                'no_log':False,
                'debug':True,
                'read':'testing/testing_alerts.binetflow'}

        detector = Detector(args)

        self.assertTrue(detector)


    # run
    def test_run__with_netflow_file_and_inverted_cmd_line_args(self):
        '''
        Testing the run function's operation, using a netflow file for input.
        Input - Dictionary of values simulating non-default output get_cmd_line_args function call.
        Requires - Websocket server to be running.
        Expected output - Returns 0
        '''
        args = {'no_gui':True,
                'no_log':True,
                'debug':True,
                'read':'testing/testing_alerts.binetflow'}

        sp = subprocess.Popen("npm start", shell=True, preexec_fn=os.setsid)

        detector = Detector(args)

        ret_val = detector.run()

        self.assertEquals(ret_val, 0)

        os.killpg(sp.pid, signal.SIGTERM)