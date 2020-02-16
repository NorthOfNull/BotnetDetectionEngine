from subprocess import Popen, PIPE

class Sniffer:
	def __init__(self):
		self.running = False

		self.initalise_netflow_sniffer()


	'''
		@returns boolean for status of sniffer
	'''
	def initalise_netflow_sniffer(self):
		# Input pipeline initialisation
		# Sniffs raw data from a SPAN'd port, performs netflow feature extraction 
		# TCPDUMP (pcap) | ARGUS (argus) | RA CLIENT (Formatted Neflow CSV Export)
		tcpdump_command = 'tcpdump -w -'
		argus_command = 'argus -f -r - -w -'
		ra_command = 'ra -c \',\' -n -s -state -s -flgs -s +1dur +8state +9stos +10dtos +sbytes'

		try:
			tcpdump = Popen(tcpdump_command, stdout=PIPE, shell=True)
			argus = Popen(argus_command, stdin=tcpdump.stdout, stdout=PIPE, shell=True)
			ra = Popen(ra_command, stdin=argus.stdout, shell=True)

			self.running = True
		except:
			# Soft error handling
			self.running = False

			raise Exception("[ Sniffer ] EXCEPTION - Netflow Collection Initalisation Failed!")

		return self.running