import websocket

'''

'''
class Websocket_Controller:
	'''

	'''
	def __init__(self):
		self.socket_addr = False
		self.socket = False

	'''

	'''
	def __del__(self):
		self.socket.close()

		print("Deleting Websocket_Controller.")

	'''
	
	'''
	def connect(self, addr):
		self.socket_addr = addr

		try:
			self.socket = websocket.create_connection(self.socket_addr)

			if(Debug):
				print("[ Websocket_Controller ] Connected to Electron!")
		except:
			raise Exception("[ Websocket_Controller ] EXCEPTION - Could not establish a connection")

	'''
	Sends the labelled_flow and alert_data as a JSON data structure through the websocket 
	'''
	def send(self, labelled_flow, alert_data):
		# Package data
		print(type(labelled_flow))
		print(type(alert_data))

		# Send data
		try:
			self.socket.send(data)
		except:
			self.attempt_reconnect()

	'''

	'''
	def attempt_reconnect(self):
		# Attempt to re-establish the Websocket connection to the server
		self.socket = None
		max_attempts = 5

		if(Debug):
			print("[ Websocket_Controller ] Connection failed.")
			print("[ Websocket_Controller ] Attempting to re-establish... ")

		for attempt in range(0, max_attempts):
			try:
				self.connect(self.socket_addr)

				print("[ Websocket_Controller ] Connection re-established!")
				break
			except:
				print("[ Websocket_Controller ] Attempt ", attempt, "failed...")
				time.sleep(2)

			if attempt == (max_attempts - 1):
				print("[ Websocket_Controller ] EXCEPTION - Could not re-esablish a connection.")
				print("--- Botnet Detection Engine Terminating ---")

				# Kills the parent process (and thus, the sniffer's subprocesses, as defined in the sniffer destructor)
				sys.exit()