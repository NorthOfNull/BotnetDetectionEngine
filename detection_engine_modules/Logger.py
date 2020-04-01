

'''

'''
class Logger:
	'''

	'''
	def __init__(self):
		self.log_file_name = "alerts.log"
		self.file = None

		self.open_file()


	'''

	'''
	def __del__(self):
		print("Deleting Logger object and closing the file handle.")

		self.file.close()


	'''
	Creates a file handle from the given file name, with the ability to write to the file.
	'''
	def open_file(self):
		# Uses 'self.log_file_name' for the file name
		# Opens file as 'self.file_handle' 
		self.file = open(self.log_file_name, 'w')

		print("[ Logger ] Log file successfully created!")

		return 0


	'''
	Writes the provided data to the file.
	'''
	def write_to_file(self, data):
		# Decode the data into utf-8 format
		flow_string = flow.decode("utf-8")

		# Write to file
		self.file.write(flow_string + "\n")

		return 0