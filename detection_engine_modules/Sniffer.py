import os
import signal
from subprocess import Popen, PIPE


'''
Sniffs raw data from the Network Interface Card (NIC), generally connected to a SPAN'd switchport.
Performs netflow feature extraction for sniffed data, or inputted '.pcap' files.
Network flow sniffing mimics bash shell behaviour of:
$ TCPDUMP (interface) | ARGUS | RA CLIENT (CSV Formatted Network Flow Exporter).

Alternative behaviour is to run offline ('.pcap' or network flow ('binetflow' or '.csv') files).
'''
class Sniffer:
	'''

	'''
	def __init__(self, read_from_file):
		self.tcpdump = None
		self.argus = None
		self.ra = None

		self.read_from_file = read_from_file
		self.file = None

		if(self.read_from_file == True):
			if '.pcap' in self.read_from_file:
				# '.pcap' file processing commands
				self.argus_command = 'argus -f -r' + read_from_file + '-w -'
				
				print("[ Sniffer ] PCAP FILE INPUT")
			elif '.binetflow' or '.csv' in self.read_from_file:
				# Network Flow File
				self.file = open(self.read_from_file)

				print("[ Sniffer ] NETWORK FLOW OR CSV FILE INPUT")
		else:
			# Network flow processing pipeline initialisation
			# ra command includes the full extended network flow feature fields required for the machine learning models
			self.tcpdump_command = 'tcpdump -w -'
			self.argus_command = 'argus -f -r - -w -'
		
		self.ra_command = 'ra -c \',\' -n -s saddr daddr proto sport dport state stos dtos swin dwin shops dhops stime ltime sttl dttl tcprtt synack ackdat spkts dpkts sbytes dbytes sappbytes dappbytes dur pkts bytes appbytes rate srate drate label'

	'''

	'''
	def __del__(self):
		if(self.file == True):
			self.file.close()
		else:
			if(self.read_from_file == False):
				# Kill tcpdump
				os.killpg(os.getpgid(self.tcpdump.pid), signal.SIGTERM)
				self.tcpdump.kill()

			# Kill argus
			os.killpg(os.getpgid(self.argus.pid), signal.SIGTERM)
			self.argus.kill()
			
			# Kill ra
			os.killpg(os.getpgid(self.ra.pid), signal.SIGTERM)
			self.ra.kill()

		print("Deleting Sniffer object and any relevant running subprocesses.")

	'''

	@returns boolean for status of sniffer
	'''
	def start(self):
		# BASE RA FIELDS COMMAND
		#ra_command = 'ra -c \',\' -n -s -state -s -flgs -s +1dur +8state +9stos +10dtos +sbytes'

		if(self.file == None):
			# If we are not reading from a pre-processed network flow file ('.binetflow' or '.csv'),
			# we setup the subprocesses accordingly for '.pcap' file or raw network data processing.
			try:
				if(self.read_from_file == True):
					# '.pcap' file subprocess setup
					self.argus = Popen(self.argus_command, stdout=PIPE, shell=True, preexec_fn=os.setsid)
				else:
					# Network sniffer subprocess setup
					# Requires tcpdump stdout to be piped into argus stdin
					self.tcpdump = Popen(self.tcpdump_command, stdout=PIPE, shell=True, preexec_fn=os.setsid)
					self.argus = Popen(self.argus_command, stdin=self.tcpdump.stdout, stdout=PIPE, shell=True, preexec_fn=os.setsid)

				# Common for both '.pcap' and network flow data processing
				# Gets stdin from argus subprocess
				self.ra = Popen(self.ra_command, stdin=self.argus.stdout, stdout=PIPE, shell=True, preexec_fn=os.setsid)

				print("[ Sniffer  ] Started network sniffer and flow processor.")
			except:
				raise Exception("[ Sniffer ] Netflow Collection Initalisation Failed!")
		else:
			print("[ Sniffer ] Reading from pre-processed file ", self.read_from_file)

		return 0


	'''
	Reads and returns stdout data from the 'ra' subprocess, or by reading the lines in the pre-processed file handle.

	Also sanitises the flow that it receivies (such as filling in empty csv fields)

	@returns a sniffed network flow; from the stdout of the 'ra' subprocess
	'''
	def get_flow(self):
		if(self.file):
			# Read line from file handle
			sniffed_flow = self.file.read()
		else:
			# For '.pcap' file or sniffer network data
			# Gets the flow data from the 'self.ra' stdout
			sniffed_flow = self.ra.stdout.readline()
	
			# Removes the newline character from the end of the
			sniffed_flow = sniffed_flow[:-1]
	
		return sniffed_flow