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

        valid_file = 'testing/testing_alerts.binetflow'

        sniffer = Sniffer(valid_file)

        self.assertTrue(sniffer)
        del sniffer

    def test_init__with_invalid_file(self):
        '''
        Testing the module's constructor.
        Input - invalid file argument.
        Expected output - Exception(FileNotFoundError)
        '''
        invalid_file = 'testing/not_a_real_file.binetflow'

        self.assertRaises(FileNotFoundError, Sniffer, invalid_file)


    # start
    def test_start__without_file(self):
        '''
        Testing the return value of the start function, without a file string being present in the object.
        Input - no file string on object instantiation.
        Expected output - sniffer.start() == true
        '''
        sniffer = Sniffer()

        started = sniffer.start()

        self.assertTrue(started)
        del sniffer

    def test_start__with_file(self):
        '''
        Testing the return value of the start function, with a file string being present in the object.
        Input - valid file string on object instantiation.
        Expected output - sniffer.start() == true
        '''
        sniffer = Sniffer('testing/testing_alerts.binetflow')

        started = sniffer.start()

        self.assertTrue(started)
        del sniffer


    # get_flow
    #def test_get_flow(self):
    #    '''
    #    Testing if get_flow returns a flow from the network (standard behaviour).
    #    Requires - the sniffer's subprocesses to be running.
    #    Expected output - A network flow received from the subprocesses.
    #    '''
    #    sniffer = Sniffer()
    #    started = sniffer.start()
    #
    #    sniffer.tcpdump_command = 'sudo tcpdump -w -'
    #    sniffer.argus_command = 'sudo argus -f -r - -w -'
    #    sniffer.ra_command = "sudo ra -c \',\' -n -s saddr daddr proto sport dport state stos dtos swin dwin shops dhops stime ltime sttl dttl tcprtt synack ackdat spkts dpkts sbytes dbytes sappbytes dappbytes dur pkts bytes appbytes rate srate drate label"
    #
    #
    #    sp = subprocess.Popen("sleep 0.5; ping -c 3 1.1.1.1", shell=True, preexec_fn=os.setsid)

    #    flow = False
    #    flow = sniffer.get_flow()
    #
    #    self.assertTrue(flow)

    #    os.killpg(sp.pid, signal.SIGTERM)
    #    del sniffer




# White box testing
class wb_SnifferTest(unittest.TestCase):
    # __init__
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
        self.assertTrue(sniffer.ra_command)

        del sniffer

    def test_init__with_valid_pcap_file_arg(self):
        '''
        Testing the module's constructor - file handling-related init variables and function calls.
        Requires - Valid packet capture file string in object.
        Expected output - Object attribute values required for a network flow input file.
        '''
        sniffer = Sniffer('testing/menti.pcap')

        self.assertEqual(sniffer.tcpdump, None)
        self.assertEqual(sniffer.argus, None)
        self.assertEqual(sniffer.ra, None)
        self.assertEqual(sniffer.read_from_file, 'testing/menti.pcap')
        self.assertFalse(sniffer.file)
        self.assertEqual(sniffer.argus_command, 'argus -f -r ' + sniffer.read_from_file + ' -w -')
        self.assertTrue(sniffer.ra_command)

        del sniffer

    def test_init__with_valid_network_flow_file_arg(self):
        '''
        Testing the module's constructor - file handling-related init variables and function calls.
        Requires - Valid network flow file string in object.
        Expected output - Object attribute values required for a network flow input file.
        '''
        sniffer = Sniffer('testing/testing_alerts.binetflow')

        self.assertEqual(sniffer.tcpdump, None)
        self.assertEqual(sniffer.argus, None)
        self.assertEqual(sniffer.ra, None)
        self.assertEqual(sniffer.read_from_file, 'testing/testing_alerts.binetflow')
        self.assertTrue(sniffer.file)
        self.assertTrue(sniffer.ra_command)

        del sniffer

    def test_init__with_invalid_file_extension(self):
        '''
        Testing the module's constructor - checking that the file read code only accept valid file extensions.
        Input - invalid file extension argument.
        Expected output - Exception
        '''
        invalid_file = 'testing/not_a_valid_file.txt'

        self.assertRaises(Exception, Sniffer, invalid_file)


    # start
    def test_start__with_no_file(self):
        '''
        Testing the return value of the start function, without a file string being present in the object.
        Requires - nothing.
        Expected output - sniffer.start() == true
        '''
        sniffer = Sniffer()

        started = sniffer.start()

        self.assertTrue(started)
        del sniffer

    def test_start__with_pcap_file(self):
        '''
        Testing the return value of the start function, with a pcap file.
        Requires - object to have a valid pcap file.
        Expected output - sniffer.start() == true
        '''
        sniffer = Sniffer('testing/menti.pcap')

        started = sniffer.start()

        self.assertTrue(started)
        del sniffer

    def test_start__with_network_flow_file(self):
        '''
        Testing the return value of the start function, with a network flow file.
        Requires - object to have a valid network flow file.
        Expected output - sniffer.start() == true
        '''
        sniffer = Sniffer('testing/menti.pcap')

        started = sniffer.start()

        self.assertTrue(started)
        del sniffer


    # get_flow
    #def test_get_flow__from_network(self):
    #    '''
    #    Testing if get_flow returns a flow from the network.
    #    Requires - the sniffer's subprocesses to be running.
    #    Expected output - A network flow received from the subprocesses.
    #    '''
    #    sniffer = Sniffer()
    #    started = sniffer.start()
    #    sniffer.tcpdump_command = 'sudo tcpdump -w -'
    #    sniffer.argus_command = 'sudo argus -f -r - -w -'
    #    sniffer.ra_command = "sudo ra -c \',\' -n -s saddr daddr proto sport dport state stos dtos swin dwin shops dhops stime ltime sttl dttl tcprtt synack ackdat spkts dpkts sbytes dbytes sappbytes dappbytes dur pkts bytes appbytes rate srate drate label"
    #
    #    sp = subprocess.Popen("sleep 0.5; ping -c 3 1.1.1.1", shell=True, preexec_fn=os.setsid)
    #
    #    flow = False
    #    flow = sniffer.get_flow()
    #
    #    print(flow)
    #
    #    self.assertTrue(flow)
    #    
    #    os.killpg(sp.pid, signal.SIGTERM)
    #    del sniffer

    def test_get_flow__from_pcap_flow_file(self):
        '''
        Testing if get_flow returns a flow from the the pcap file.
        Requires - the sniffer's subprocesses to be running.
        Expected output - A processed network flow from the packet capture file.
        '''
        sniffer = Sniffer('testing/menti.pcap')
        started = sniffer.start()

        flow = sniffer.get_flow()

        self.assertTrue(flow)

        del sniffer

    def test_get_flow__from_network_flow_file(self):
        '''
        Testing if get_flow returns a flow from the network flow file.
        Requires - the sniffer's subprocesses to be running and have a valid file handle.
        Expected output - A network flow read from the file.
        '''
        sniffer = Sniffer('testing/testing_alerts.binetflow')
        started = sniffer.start()

        flow = sniffer.get_flow()

        self.assertTrue(flow)

        del sniffer

    def test_get_flow__reach_EOF(self):
        '''
        Testing if get_flow returns False when reaching End-of-file (EOF)
        Requires - the sniffer's subprocesses to be running and have a valid file handle.
        Expected output - get_flow returns False when EOF is reached.
        '''
        sniffer = Sniffer('testing/testing_alerts.binetflow')
        started = sniffer.start()

        flow = sniffer.get_flow()
        flow = sniffer.get_flow()
        flow = sniffer.get_flow()
        flow = sniffer.get_flow()
        flow = sniffer.get_flow()
        flow = sniffer.get_flow()
        flow = sniffer.get_flow()

        self.assertFalse(flow)

        del sniffer
