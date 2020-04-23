import sys
import time
import websocket

'''

'''
class Websocket_Client:
	'''

	'''
	def __init__(self):
		self.socket_addr = False
		self.socket = False

	'''

	'''
	def __del__(self):
		if self.socket is not False:
			self.socket.close()

		print("Deleting Websocket Client.")

	'''
	
	'''
	def connect(self, socket_addr):
		self.socket_addr = socket_addr

		try:
			self.socket = websocket.create_connection(self.socket_addr)

			print("[ Websocket_Client ] Connected to Electron!")
		except:
			raise Exception("[ Websocket_Client ] EXCEPTION - Could not establish a connection")

	'''
	Sends the labelled_flow and alert_data as a JSON data structure through the websocket 
	'''
	def send(self, labelled_flow, alert):
		# Package data

		# Package labelled_flow and alert together

		# TODO
		# TODO
		# TODO

		data = labelled_flow


		# Send data
		try:
			self.socket.send(data)
		except:
			self.attempt_reconnect()

	'''

	'''
	def attempt_reconnect(self):
		# Attempt to re-establish the Websocket connection to the server
		self.socket = False
		max_attempts = 5

		print("[ Websocket_Client ] Connection failed.")
		print("[ Websocket_Client ] Attempting to re-establish... ")

		for attempt in range(0, max_attempts):
			try:
				self.connect(self.socket_addr)

				print("[ Websocket_Client ] Connection re-established!")
				break
			except:
				print("[ Websocket_Client ] Attempt ", attempt, "failed...")
				time.sleep(2)

			if attempt == (max_attempts - 1):
				print("[ Websocket_Client ] ] EXCEPTION - Could not re-esablish a connection.")
				print("--- Botnet Detection Engine Terminating ---")

				# Kills the parent process (and thus, the sniffer's subprocesses, as defined in the sniffer destructor)
				sys.exit()

		return self.socket