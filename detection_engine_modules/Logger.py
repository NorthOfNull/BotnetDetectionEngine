

'''
Logs labelled flows and alerts
'''
class Logger:
	'''

	'''
	def __init__(self):
		self.flow_file = None
		self.alert_file = None

		self.flow_file_name = "flows.binetflow"
		self.alert_file_name = "alerts.log"

		self.open_flow_file()
		self.open_alert_file()

	'''

	'''
	def __del__(self):
		print("Deleting Logger object and closing the file handle.")

		if self.flow_file and self.alert_file:
			close(self.flow_file)
			close(self.alert_file)

	'''
	Creates a file handle for the flow log file, with the ability to write to the file.
	'''
	def open_flow_file(self):
		# Uses 'self.flow_file_name' for the file name
		# Opens writeable file as 'self.file_handle' 
		self.file = open(self.flow_file_name, 'w')

		print("[ Logger ] Network Flow file successfully opened!")

		return 0

	'''
	Writes the flow data to the file.
	'''
	def write_flow_to_file(self, flow):
		# Decode the data into utf-8 format
		flow_string = flow.decode("utf-8")

		# Write to file
		self.file.write(flow_string + "\n")

		return 0

	'''
	Creates a file handle for the alert log, with the ability to write to the file.
	'''
	def open_alert_file(self):
		# Uses 'self.alert_file_name' for the file name
		# Opens writeable file as 'self.file_handle' 
		self.file = open(self.alert_file_name, 'w')

		print("[ Logger ] Alert file successfully opened!")

		return 0

	'''
	Writes the alert data to the file.
	'''
	def write_alert_to_file(self, alert):
		# Decode the data into utf-8 format
		#alert = flow.decode("utf-8")

		# Write to file
		self.file.write(flow_string + "\n")

		return 0

