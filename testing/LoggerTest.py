import unittest

from detection_engine_modules.Logger import Logger

class bb_LoggerTest(unittest.TestCase):
	def test_Error(self):
		'''

		'''
		logger = Logger()
		input = ""

		retVal = logger.write_flow_to_file(input)
		self.assertFalse(retVal)


class wb_LoggerTest(unittest.TestCase):
	def test_Error(self):
		'''

		'''
		logger = Logger()
		input = ""

		retVal = logger.write_flow_to_file(input)
		self.assertFalse(retVal)