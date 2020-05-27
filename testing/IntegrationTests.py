import unittest


from detection_engine_modules.Detector import Detector

#
# Integration testing file.
#
# Note - this is not the full integration testing; only an automated subset!
#      - full integration tests are not fully conducted using unittest automation.
#

# Black box testing
class IntegrationTesting(unittest.TestCase):
    def test_detector__with_negative_test_data(self):
        '''
        Testing Detector behaviour with known negative test data.
        Input - Known negative test data = "31.149.113.113,147.32.84.229,tcp,60046,443,RST,0.0,0.0,524280.0,65535.0,17.0,1.0,2011/08/16 14:03:51.019116,2011/08/16 14:03:51.204569,47.0,127.0,0.000218,0.000218,0.0,2,1,126,66,0,0,0.185453,3,192,0,10.784403999999999,5.392201999999999,0.0,"
        Requires - A detector object to be running.
        Expected output - Return a false 'Normal' labelled prediction and false alert.
        '''
        args = {'no_gui':True,
                'no_log':True,
                'debug':False,
                'read':False}

        detector = Detector(args)

        known_negative_test_data = "31.149.113.113,147.32.84.229,tcp,60046,443,RST,0.0,0.0,524280.0,65535.0,17.0,1.0,2011/08/16 14:03:51.019116,2011/08/16 14:03:51.204569,47.0,127.0,0.000218,0.000218,0.0,2,1,126,66,0,0,0.185453,3,192,0,10.784403999999999,5.392201999999999,0.0,"
        flow = detector.process_flow(known_negative_test_data)

        prediction, alert = detector.predict(flow)

        self.assertEqual(prediction, 'Normal')
        self.assertFalse(alert)

    def test_detector__with_positive_test_data(self):
        '''
        Testing Detector behaviour with known positive test data.
        Input - Known positive test data = "147.32.53.111,66.111.4.72,tcp,3907,25,REQ,0.0,0.0,64240.0,0.0,1.0,0.0,2011/08/17 15:41:06.125672,2011/08/17 15:41:15.153223,127.0,0.0,0.0,0.0,0.0,3,0,186,0,0,0,9.027550999999999,3,186,0,0.22154400000000002,0.22154400000000002,0.0,""
        Requires - A detector object to be running.
        Expected output - Return a true 'Botnet' labelled prediction and returns a non-false alert value.
        '''
        args = {'no_gui':True,
                'no_log':True,
                'debug':False,
                'read':False}

        detector = Detector(args)

        known_positive_test_data = "147.32.53.111,66.111.4.72,tcp,3907,25,REQ,0.0,0.0,64240.0,0.0,1.0,0.0,2011/08/17 15:41:06.125672,2011/08/17 15:41:15.153223,127.0,0.0,0.0,0.0,0.0,3,0,186,0,0,0,9.027550999999999,3,186,0,0.22154400000000002,0.22154400000000002,0.0,"
        flow = detector.process_flow(known_positive_test_data)

        prediction, alert = detector.predict(flow)

        self.assertEqual(prediction, 'Botnet')
        self.assertTrue(alert)



    def test_detector__with_binetflow_test_file(self):
        '''
        Testing Detector behaviour with test binetflow file.
        Input - Valid object init arguments, with the test binetflow file provided.
        Requires - Nothing.
        Expected output - Successfully runs the detector and returns 0 on successful exit.
        '''
        args = {'no_gui':True,
                'no_log':True,
                'debug':False,
                'read':'testing/testing_alerts.binetflow'}

        detector = Detector(args)
        ret = detector.run()

        self.assertEqual(ret, 0)