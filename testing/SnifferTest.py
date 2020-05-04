import unittest

import os, signal, subprocess

from detection_engine_modules.Sniffer import Sniffer

#
# Sniffer module testing file.
#

# Black box testing
class bb_SnifferTest(unittest.TestCase):
	def test_init__no_arg(self):
		'''
		Testing the module's constructor.
		Input - no argument.
		Expected output - successful sniffer object instantiation.
		'''
		sniffer = False
		sniffer = Sniffer()

		self.assertTrue(sniffer)
		del sniffer

	def test_init__with_valid_arg(self):
		'''
		Testing the module's constructor.
		Input - a valid file argument.
		Expected output - successful sniffer object instantiation.
		'''
		sniffer = False

		valid_file = 'testing_alerts.binetflow'

		sniffer = Sniffer(valid_file)

		self.assertTrue(sniffer)
		del sniffer

	def test_init__with_invalid_file(self):
		'''
		Testing the module's constructor.
		Input - invalid file argument.
		Expected output - Exception(FileNotFoundError)
		'''
		sniffer = False

		invalid_file = 'not_a_real_file.binetflow'

		self.assertRaises(FileNotFoundError, Sniffer, invalid_file)
		del sniffer


	# start
	def test_start__without_file(self):
		'''
		Testing the return value of the start function, without a file string being present in the object.
		Input - no file string on object instantiation.
		Expected output - sniffer == true
		'''
		sniffer = Sniffer()

		started = sniffer.start()

		self.assertTrue(started)
		del sniffer

	def test_start__with_file(self):
		'''
		Testing the return value of the start function, with a file string being present in the object.
		Input - valid file string on object instantiation.
		Expected output - sniffer == true
		'''
		sniffer = Sniffer('testing_alerts.binetflow')

		started = sniffer.start()

		self.assertTrue(started)
		del sniffer


	# get_flow
	def test_get_flow(self):
		'''
		Testing if get_flow returns a flow from the network (standard behaviour).
		Requires - the sniffer's subprocesses to be running.
		Expected output - A network flow received from the subprocesses.
		'''
		sniffer = Sniffer()
		started = sniffer.start()

		sp = subprocess.Popen("ping -c 3 1.1.1.1", shell=True, preexec_fn=os.setsid)

		flow = False
		flow = sniffer.get_flow()

		self.assertTrue(flow)

		os.killpg(sp.pid, signal.SIGTERM)
		del sniffer




# White box testing
class wb_SnifferTest(unittest.TestCase):
	def test_init__no_arg(self):
		'''
		Testing the module's constructor - default init variables and function calls.
		Input - No argument.
		Expected output - Default object attribute values.
		'''
		sniffer = Sniffer()

		self.assertEqual(sniffer.tcpdump, None)
		self.assertEqual(sniffer.argus, None)
		self.assertEqual(sniffer.ra, None)
		self.assertEqual(sniffer.read_from_file, False)
		self.assertEqual(sniffer.file, None)
		self.assertEqual(sniffer.tcpdump_command, 'tcpdump -w -')
		self.assertEqual(sniffer.argus_command, 'argus -f -r - -w -')
		self.assertEqual(sniffer.ra_command, 'ra -c \',\' -n -s saddr daddr proto sport dport state stos dtos swin dwin shops dhops stime ltime sttl dttl tcprtt synack ackdat spkts dpkts sbytes dbytes sappbytes dappbytes dur pkts bytes appbytes rate srate drate label')

		del sniffer

	def test_init__with_valid_flow_file_arg(self):
		'''
		Testing the module's constructor - file handling-related init variables and function calls.
		Input - Valid network flow file string.
		Expected output - Object attribute values required for a network flow input file.
		'''
		sniffer = Sniffer('testing_alerts.binetflow')

		self.assertEqual(sniffer.tcpdump, None)
		self.assertEqual(sniffer.argus, None)
		self.assertEqual(sniffer.ra, None)
		self.assertEqual(sniffer.read_from_file, 'testing_alerts.binetflow')
		self.assertTrue(sniffer.file)
		self.assertEqual(sniffer.ra_command, 'ra -c \',\' -n -s saddr daddr proto sport dport state stos dtos swin dwin shops dhops stime ltime sttl dttl tcprtt synack ackdat spkts dpkts sbytes dbytes sappbytes dappbytes dur pkts bytes appbytes rate srate drate label')

		del sniffer


	# start

	## TODO 
	## TODO
	## TODO
	### with file
	### without file
	### wrong file


	# get_flow
	def test_get_flow__from_network(self):
		'''
		Testing if get_flow returns a flow from the network.
		Requires - the sniffer's subprocesses to be running.
		Expected output - A network flow received from the subprocesses.
		'''
		sniffer = Sniffer()
		started = sniffer.start()

		flow = False

		sp = subprocess.Popen("ping -c 3 1.1.1.1", shell=True, preexec_fn=os.setsid)

		flow = sniffer.get_flow()

		print(flow)

		self.assertTrue(flow)
		
		os.killpg(sp.pid, signal.SIGTERM)
		del sniffer

	def test_get_flow__from_file(self):
		'''
		Testing if get_flow returns a flow from the a file.
		Requires - the sniffer's subprocesses to be running.
		Expected output - A network flow received from the file.
		'''