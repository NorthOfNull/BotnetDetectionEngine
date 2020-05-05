import unittest

from detection_engine_modules.Logger import Logger

#
# Logger module testing file.
#

# Black box testing
class bb_LoggerTest(unittest.TestCase):
    def test_init(self):
        '''
        Testing the module's constructor.
        Input - none.
        Expected output - successful logger object instantiation.
        '''
        logger = False
        logger = Logger()

        self.assertTrue(logger)


    # open_flow_file
    def test_open_flow_file(self):
        '''
        Testing the flow file open function.
        '''
        logger = Logger()

        self.assertEqual(logger.open_flow_file(), 0)


    # write_flow_to_file
    def test_write_flow_to_file(self):
        '''
        Testing the write flow to file function, with a string.
        Requires - a file handle to be opened by the object.
        '''
        logger = Logger()

        flow = "test"
        ret = logger.write_flow_to_file(flow)

        self.assertEqual(ret, 0)

    def test_write_flow_to_file__empty_string(self):
        '''
        Testing the write flow to file function, with an empty string.
        Requires - a file handle to be opened by the object.
        '''
        logger = Logger()

        flow = ""
        ret = logger.write_flow_to_file(flow)

        self.assertEqual(ret, 0)

    def test_write_flow_to_file__no_string(self):
        '''
        Testing the write flow to file function, without a string.
        Requires - a file handle to be opened by the object.
        '''
        logger = Logger()

        self.assertRaises(TypeError, logger.write_flow_to_file)


    # open_alert_file
    def test_open_alert_file(self):
        '''
        Testing the alert file open function.
        '''
        logger = Logger()

        self.assertEqual(logger.open_alert_file(), 0)


    # write_alert_to_file
    def test_write_alert_to_file(self):
        '''
        Testing the write alert to file function, with a json object.
        Requires - a file handle to be opened by the object.
        '''
        logger = Logger()

        alert = {
            "test1":{"0":0,
                     "1":1
                    },
            "test2":{"2":2,
                     "3":3
                    }
        }
        ret = logger.write_alert_to_file(alert)

        self.assertEqual(ret, 0)

    def test_write_alert_to_file__empty_json(self):
        '''
        Testing the write alert to file function, with an empty json object.
        Requires - a file handle to be opened by the object.
        '''
        logger = Logger()

        alert = {}
        ret = logger.write_alert_to_file(alert)

        self.assertEqual(ret, 0)

    def test_write_alert_to_file__no_json(self):
        '''
        Testing the write alert to file function, without a json object.
        Requires - a file handle to be opened by the object.
        '''
        logger = Logger()

        self.assertRaises(TypeError, logger.write_alert_to_file)




# White box testing
class wb_LoggerTest(unittest.TestCase):
    def test_init(self):
        '''
        Testing the module's constructor - init variables and function calls.
        Expected output:
            logger.alert_no == 1
            logger.flow_file == True
            logger.alert_file == True
            logger.flow_file_name == 'flows.binetflow'
            logger.alert_file_name == 'alerts.log'
        '''
        logger = Logger()

        self.assertEqual(logger.alert_no, 1)
        self.assertTrue(logger.flow_file)
        self.assertTrue(logger.alert_file)
        self.assertEqual(logger.flow_file_name, 'flows.binetflow')
        self.assertEqual(logger.alert_file_name, 'alerts.log')

    # write_alert_to_file
    def test_write_alert_to_file__alert_no_increment(self):
        '''
        Ensuring the alert number is incremented correctly upon writing to file.
        Requires - an alert to be correctly processed and written to file.
        Input - valid json.
        Expected output:
            logger.write_alert_to_file(alert) == 0
            logger.alert_no == 2
        '''
        logger = Logger()
        
        alert = {
            "test1":{"0":0,
                     "1":1
                    },
            "test2":{"2":2,
                     "3":3
                    }
        }
        ret = logger.write_alert_to_file(alert)

        self.assertEqual(ret, 0)
        self.assertEqual(logger.alert_no, 2)
