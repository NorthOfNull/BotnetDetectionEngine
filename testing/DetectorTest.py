import unittest

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

        detector = False
        detector = Detector(args)

        self.assertTrue(detector)

        detector.ws_client.socket.close()


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

        detector = Detector(args)

        ret_val = detector.run()

        self.assertEqual(ret_val, 0)


    # process_flow
    def test_process_flow__with_argus_headers(self):
        '''
        Testing the process flow function's behaviour when it encounters column header labels.
        Input - Argus column header labels string.
        Requires - A Detector object.
        Expected output - Returns False.
        '''
        input_data = 'SrcAddr,DstAddr,Proto,Sport,Dport,State,sTos,dTos,SrcWin,DstWin,sHops,dHops,StartTime,LastTime,sTtl,dTtl,TcpRtt,SynAck,AckDat,SrcPkts,DstPkts,SrcBytes,DstBytes,SAppBytes,DAppBytes,Dur,TotPkts,TotBytes,TotAppByte,Rate,SrcRate,DstRate,Label'

        args = {'no_gui':True,
                'no_log':True,
                'debug':False,
                'read':'testing/testing_alerts.binetflow'}

        detector = Detector(args)

        ret = detector.process_flow(input_data)

        self.assertFalse(ret)

    def test_process_flow__with_valid_flow_data(self):
        '''
        Testing the process flow function's behaviour when it encounters non-column header network flow data.
        Input - Network flow data string.
        Requires - A Detector object.
        Expected output - Returns a valid Dataframe object.
        '''
        input_data = '147.32.53.111,66.111.4.72,tcp,3907,25,REQ,0.0,0.0,64240.0,0.0,1.0,0.0,2011/08/17 15:41:06.125672,2011/08/17 15:41:15.153223,127.0,0.0,0.0,0.0,0.0,3,0,186,0,0,0,9.027550999999999,3,186,0,0.22154400000000002,0.22154400000000002,0.0,'

        args = {'no_gui':True,
                'no_log':True,
                'debug':False,
                'read':'testing/testing_alerts.binetflow'}

        detector = Detector(args)

        ret = detector.process_flow(input_data)

        self.assertEqual(str(type(ret)), '<class \'pandas.core.frame.DataFrame\'>')
        
    # generate_alert
    def test_generate_alert__with_botnet_prediction(self):
        '''
        Testing the generate alert functionality when in the presence of a botnet prediction.
        Input - A flow DataFrame, it's prediction and valid model metadata.
        Requires - A Detector object.
        Expected output - A json-formatted alert.
        '''
        input_data = '147.32.53.111,66.111.4.72,tcp,3907,25,REQ,0.0,0.0,64240.0,0.0,1.0,0.0,2011/08/17 15:41:06.125672,2011/08/17 15:41:15.153223,127.0,0.0,0.0,0.0,0.0,3,0,186,0,0,0,9.027550999999999,3,186,0,0.22154400000000002,0.22154400000000002,0.0,'

        args = {'no_gui':True,
                'no_log':True,
                'debug':False,
                'read':'testing/testing_alerts.binetflow'}

        detector = Detector(args)

        flow = detector.process_flow(input_data)
        prediction, alert = detector.predict(flow)

        self.assertTrue(alert)

    def test_generate_alert__with_normal_prediction(self):
        '''
        Testing the generate alert functionality when in the presence of a normal prediction.
        Input - A flow DataFrame, it's prediction and valid model metadata.
        Requires - A Detector object.
        Expected output - Returns False.
        '''
        input_data = '31.149.113.113,147.32.84.229,tcp,60046,443,RST,0.0,0.0,524280.0,65535.0,17.0,1.0,2011/08/16 14:03:51.019116,2011/08/16 14:03:51.204569,47.0,127.0,0.000218,0.000218,0.0,2,1,126,66,0,0,0.185453,3,192,0,10.784403999999999,5.392201999999999,0.0,'

        args = {'no_gui':True,
                'no_log':True,
                'debug':False,
                'read':'testing/testing_alerts.binetflow'}

        detector = Detector(args)

        flow = detector.process_flow(input_data)
        prediction, alert = detector.predict(flow)

        self.assertFalse(alert)

    # flow_feature_exclusion
    def test_flow_feature_exclusion__with_invalid_flow(self):
        '''
        Testing how invalid flow data is handled.
        Input - Non-dataframe data.
        Requires - A Detector object
        Expected output - Raises exception.
        '''
        input_data = "non-dataframe string data"

        args = {'no_gui':True,
                'no_log':True,
                'debug':False,
                'read':'testing/testing_alerts.binetflow'}

        detector = Detector(args)

        import pandas as pd
        df = pd.DataFrame([input_data]) 

        self.assertRaises(Exception, detector.flow_feature_exclusion, input_data)
