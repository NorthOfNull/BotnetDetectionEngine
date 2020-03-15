from subprocess import Popen, PIPE


'''

'''
class Sniffer:
	'''

	'''
	def __init__(self):
		self.running = False


	'''

	'''
	def __del__(self):
		print("Deleting Sniffer Object.")


	'''
	@returns boolean for status of sniffer
	'''
	def start(self):
		# Input pipeline initialisation
		# Sniffs raw data from a SPAN'd port, performs netflow feature extraction 
		# TCPDUMP (pcap) | ARGUS (argus) | RA CLIENT (Formatted Neflow CSV Export)
		tcpdump_command = 'tcpdump -w -'
		argus_command = 'argus -f -r - -w -'
		ra_command = 'ra -c \',\' -n -s saddr daddr proto sport dport state stos dtos swin dwin shops dhops stime ltime sttl dttl tcprtt synack ackdat spkts dpkts sbytes dbytes sappbytes dappbytes dur pkts bytes appbytes rate srate drate label'


		# BASE RA FIELDS COMMAND
		#ra_command = 'ra -c \',\' -n -s -state -s -flgs -s +1dur +8state +9stos +10dtos +sbytes'


		try:
			self.tcpdump = Popen(tcpdump_command, stdout=PIPE, shell=True)
			self.argus = Popen(argus_command, stdin=self.tcpdump.stdout, stdout=PIPE, shell=True)
			self.ra = Popen(ra_command, stdin=self.argus.stdout, stdout=PIPE, shell=True)

			self.running = True
		except:
			# Soft error handling
			self.running = False

			raise Exception("[ Sniffer ] EXCEPTION - Netflow Collection Initalisation Failed!")

		return True


	'''
	@returns a snniffed flows; these come from the piped stdout of the 'self.ra' subprocess
	'''
	def get_flows(self):
		# Gets the flow data from the 'self.ra' stdout
		sniffed_flow = self.ra.stdout.readline()

		# Removes the newline character from the end of the
		sniffed_flow = sniffed_flow[:-1]

		return sniffed_flow