"""
The Sniffer Module.
"""

import os
import sys
import signal
from subprocess import Popen, PIPE


class Sniffer:
    '''
    Sniffs raw data from the Network Interface Card (NIC), generally connected to a
    SPAN'd switchport.

    Performs netflow feature extraction for sniffed data, or inputted '.pcap' files.

    Network flow sniffing mimics bash shell behaviour of:
    $ TCPDUMP (interface) | ARGUS | RA CLIENT (CSV Formatted Network Flow Exporter).

    Alternative behaviour is to run offline ('.pcap' or network flow ('binetflow'
    or '.csv') files).
    '''

    def __init__(self, read_from_file=False):
        '''

        '''
        self.tcpdump = None
        self.argus = None
        self.ra = None

        self.read_from_file = read_from_file
        self.file = None

        if self.read_from_file is not False:
            if '.pcap' in self.read_from_file:
                # '.pcap' file processing command
                self.argus_command = 'argus -f -r ' + self.read_from_file + ' -w -'

                print("[ Sniffer ] Packet Capture file input detected!")
            elif '.binetflow' in self.read_from_file or '.csv' in self.read_from_file:
                # Network Flow File
                self.file = open(self.read_from_file)

                print("[ Sniffer ] Network flow file (csv or binetflow) input detected!")
            else:
                raise Exception("File type is incorrect! Expecting '.pcap', '.csv' or '.binetflow files!""")
        else:
            # Network flow processing pipeline initialisation
            # ra command includes the full extended network flow feature fields
            # required for the machine learning models
            self.tcpdump_command = 'tcpdump -w -'
            self.argus_command = 'argus -f -r - -w -'

        self.ra_command = "ra -c \',\' -n -s saddr daddr proto sport dport state stos dtos swin dwin shops dhops stime ltime sttl dttl tcprtt synack ackdat spkts dpkts sbytes dbytes sappbytes dappbytes dur pkts bytes appbytes rate srate drate label"

    '''

    '''
    def __del__(self):
        '''
        Sniffer destructor - specifically sends SIGTERM to the subprocess' PGID's.

        '''
        if(self.read_from_file == False):
            if self.tcpdump is not None:
                # Kill tcpdump
                os.killpg(self.tcpdump.pid, signal.SIGTERM)

        if self.argus is not None:
            # Kill argus
            os.killpg(self.argus.pid, signal.SIGTERM)

        if self.ra is not None:
            # Kill ra
            os.killpg(self.ra.pid, signal.SIGTERM)

        print("Deleting Sniffer object and any relevant running subprocesses.")

    '''
    Starts the required subprocesses for the sniffer.
    Operation depends on the sniffer object's attribute values.

    @returns boolean for status of sniffer
    '''
    def start(self):
        # BASE RA FIELDS COMMAND
        #ra_command = 'ra -c \',\' -n -s -state -s -flgs -s +1dur +8state +9stos +10dtos +sbytes'

        started = False

        if(self.file == None):
            # If we are not reading from a pre-processed network flow file ('.binetflow' or '.csv'),
            # we setup the subprocesses accordingly for '.pcap' file or raw network data processing.
            if self.read_from_file is not False:
                # '.pcap' file subprocess setup
                self.argus = Popen(self.argus_command, stdout=PIPE, shell=True,
                                   preexec_fn=os.setsid)
            else:
                # Network sniffer subprocess setup
                # Requires tcpdump stdout to be piped into argus stdin
                self.tcpdump = Popen(self.tcpdump_command, stdout=PIPE, shell=True,
                                     preexec_fn=os.setsid)
                self.argus = Popen(self.argus_command, stdin=self.tcpdump.stdout,
                                   stdout=PIPE, shell=True, preexec_fn=os.setsid)

            # Common for both '.pcap' and network flow data processing
            # Gets stdin from argus subprocess
            self.ra = Popen(self.ra_command, stdin=self.argus.stdout, stdout=PIPE,
                            shell=True, preexec_fn=os.setsid)

            print("[ Sniffer  ] Started network sniffer and flow processor.")
        else:
            print("[ Sniffer ] Reading from pre-processed file =", self.read_from_file)

        started = True

        return started

    '''
    Reads and returns stdout data from the 'ra' subprocess (for .pcap files or raw tcpdump
    network data), or by reading the lines in the pre-processed file handle.

    Also sanitises the flow that it receivies (such as filling in empty csv fields).

    @returns a sniffed network flow; from the stdout of the 'ra' subprocess
    '''
    def get_flow(self):
        if self.file is not None:
            # Read line from network flow file handle
            sniffed_flow = self.file.readline()

            if(len(sniffed_flow) == 0):
                # End of File
                print("[ Sniffer ] Reached EOF.")

                sniffed_flow = False
        else:
            # For '.pcap' file or sniffed network data
            # Gets the flow data from the 'self.ra' stdout
            sniffed_flow = self.ra.stdout.readline()

            # Decode the flow data into utf-8
            sniffed_flow = sniffed_flow.decode('utf-8')

        if sniffed_flow:
            if sniffed_flow[-1] == '\n':
                # Removes the newline character from the end of the line, if present
                sniffed_flow = sniffed_flow[:-1]

        return sniffed_flow
