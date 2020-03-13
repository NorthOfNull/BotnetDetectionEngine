import websocket


###
class Websocket_Controller:
	def __init__(self):
		self.socket_addr = False
		self.socket = False


	###
	def connect(self, addr):
		self.socket_addr = addr

		try:
			self.socket = websocket.create_connection(self.socket_addr)

			print("[ Websocket_Controller ] Connected to Electron!")
		except:
			raise Exception("[ Websocket_Controller ] EXCEPTION - Could not esablish a connection")

