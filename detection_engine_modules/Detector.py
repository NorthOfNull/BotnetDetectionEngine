# init
#	self.model_dir
#	self.models (array of de-serialised model objects)

# del

# load_models(self) (de-serialise (de-pickle) the models from the directory)

# predict(self, flow)
#	for model in self.models:
#		prediction = predict(flow)
#   	flow = flow.append(prediction)
#	
#	return flow


import os
import json
import pandas as pd

from detection_engine_modules.Model import Model
from detection_engine_modules.Logger import Logger
from detection_engine_modules.Sniffer import Sniffer
from detection_engine_modules.Websocket_Client import Websocket_Client


'''

'''
class Detector:
	'''

	'''
	def __init__(self, args):
		self.GUI = args.no_gui
		self.Logging = args.no_log
		self.Debug = args.debug
		self.Read = args.read

		self.dataset_feature_columns = ['SrcAddr', 'DstAddr', 'Proto', 'Sport', 'Dport', 'State',
			'sTos', 'dTos', 'SrcWin', 'DstWin', 'sHops', 'dHops', 'StartTime', 'LastTime', 'sTtl',
			'dTtl', 'TcpRtt', 'SynAck', 'AckDat', 'SrcPkts', 'DstPkts', 'SrcBytes', 'DstBytes',
			'SAppBytes', 'DAppBytes', 'Dur', 'TotPkts', 'TotBytes', 'TotAppByte', 'Rate', 'SrcRate',
			'DstRate']

		self.models = []
		self.model_directory = 'Models'
		self.socket_addr = "ws://localhost:5566"


		if(self.Debug):
			print("[ Detector ] Debugging enabled.")

		# De-serialise model objects into the model array
		self.models = self.load_models()

		# Sniffs raw data from a SPAN'd port, performs netflow feature extraction.
		# Mimics bash shell behaviour of:
		# $ TCPDUMP (interface) | ARGUS | RA CLIENT (CSV Formatted Network Flow Exporter).
		self.sniffer = Sniffer(self.Read)

		if(self.GUI == True):
			# Websocket_Client instance
			# Faciliates data transfer through a localhost socket to the backend electron nodejs server
			# Create websocket connection to the nodejs websocket server
			self.ws_client = Websocket_Client()

			# And attempt to connect to the websocker server
			self.ws_client.connect(self.socket_addr)

		if(self.Logging == True):
			# Flow and Alert file logging
			# Initialise Logger instance to handle alert and flow file logging operations
			self.logger = Logger()

	'''

	'''
	def __del__(self):
		if(self.Debug == True):
			print("Deleting Detector object and the loaded models.")


	'''
	Main running loop for the detector.
	Gets flows from the network flow sniffer, predicts the behaviour via the models and outputs the data
	'''
	def run(self):
		# Start sniffer
		self.sniffer.start()

		# Main loop
		while(True):
			flow_string = None
			flow = None
			labelled_flow = None
			alert = None

			# Get raw flow string from the sniffer instance
			# Gets flow data from the a processed .pcap file, .binetflow csv file or from the network interface
			flow_string = self.sniffer.get_flow()

			# Process the flow_string into a DataFrame with the required feature vectors being maintained
			# So that the flow data is ready to make predictions
			flow = self.process_flow(flow_string)

			# If there is a valid flow (i.e. self.process_flow successfully returns a processed_flow)
			if flow is not False:
				# Predict the flow's class, using the detector's models
				# Takes the DataFrame network flow data and predicts against each model
				prediction, alert = self.predict(flow)

				# Make labelled_flow string
				labelled_flow = flow_string + prediction
			else:
				# Not flow data, i.e. the data is that of the feature headers
				labelled_flow = flow_string

			# Output the labelled flow to stdout
			print(labelled_flow + "\n")


			# If GUI is enabled
			if(self.GUI == True):
				# Send the flow and any alert data to the GUI instance, via the websocket
				self.ws_client.send(labelled_flow, alert)
			
			# If Logging is enabled
			if(self.Logging == True):
				# Log the labelled flow output to the file
				self.logger.write_flow_to_file(labelled_flow)

				if(alert != None):
					self.logger.write_alert_to_file(alert)

		return 0

	'''
	De-serialisation of trained Machine Learning models that are contained in the 'Models' directory.
	Loaded objects get stored in the 'self.models' array, along with their descriptive data.

	'''
	def load_models(self):
		models = []
		model_data = None

		if(self.Debug):
			print("[ Detector ] Loading Models...")

		# Handle nothing being present in directory
		# Handle directory not being present
		assert(os.path.exists(self.model_directory))

		# Get model metadata from the json file
		data_file = self.model_directory + '/model_data.json'
		model_json_metadata = self.get_model_data(data_file)


		# Load models that have file names present within the model_json_metadata file (filenames are stored as the json keys)
		for model_file_name in model_json_metadata.keys():
			# Instantiate model object, with the full relative model file path being passed as an argument
			model_data = model_json_metadata[model_file_name]

			instance_of_model = Model(self.model_directory, model_file_name, model_data)

			if(instance_of_model.loading_status == True):
				# If the model is succesfully loaded
				# Add the model object to the Detector
				models.append(instance_of_model)
			else:
				# Object cleanup
				del instance_of_model

		if(self.Debug):
			print("[ Detector ] Loaded", len(models), "/", len(model_json_metadata.keys()), "models.")

		if(len(models) == 0):
			raise Exception("[ Detector ] Model Loading Failed")

		return models

	'''
	Processes flow_string into the valid DataFrame, with the column headers included.

	@returns The flow DataFrame
	'''
	def process_flow(self, flow_string):
		if 'Label' in flow_string:
			# Not a valid flow ('ra' client flow feature headers)
			processed_flow = False
		else:
			# Split flow_string into array
			flow = flow_string.split(',')

			# Remove the last empty 'label' data field from the flow 
			flow.pop()

			# Fill in empty csv fields
			for i, data in enumerate(flow):
				if not data:
					flow[i] = 0

			# Process into DataFrame, with the relative dataset feature column headers
			processed_flow = pd.DataFrame([flow], columns=self.dataset_feature_columns)

		return processed_flow

	'''
	Predicts the label of the given network flow data.
	If the flow is predicted as botnet, we return the data about the models that made the prediction.

	@returns The prediction verdict ('Normal' or 'Botnet')
	@returns The json model data, in the form of an alert, from positive models.
	'''
	def predict(self, flow):
		# Predict the label of the flow using each loaded model
		original_flow = flow
		alert = None
		prediction = None
		predicted_model_data = []

		# Flow feature exclusion
		# Required to only pass valid the model feature vector (the features that the models were trained on)
		# to the models, ready for prediction
		flow = self.flow_feature_exclusion(flow)

		# Iterate over each running model instance, making predictions on each
		for model in self.models:
			model_prediction = model.predict(flow)

			if(model_prediction == 'Botnet'):
				# Botnet prediciton
				# Add model data to the array
				predicted_model_data.append(model.model_metadata)


		if(len(predicted_model_data) > 0):
			# If we have any positive predicitons
			# Label overall prediciton as 'Botnet'
			prediction = 'Botnet'

			# And generate an alert, filled with relevant flow data and the exhibited botnet-like characteristics of the traffic
			alert = generate_alert(original_flow, predicted_model_data)
		else:
			prediction = 'Normal'


		print("PREDICTION =", prediction)

		if(self.Debug and prediction == 'Botnet'):
			print("Overall prediction =", prediction)
			print("Predicted model metadata =", predicted_model_data)



		# TODO
		# get 'bot_alert_data' from the model object's data that is loaded from the json file that stores model characteristic data
		# we will use this data in the logging process within the Logger module, generating the alerts

		return prediction, alert

	'''
	Generates an alert data structure from the specific data of each positive prediction model.

	@returns The generated alert data
	'''
	def generate_alert(self, original_flow, predicted_model_data):
		alert = "!!!!!!!GENERATING ALERT!!!!!!!!"

		print(alert)


		# get 'predicted_model_data' from the model object's data that is loaded from the json file that stores model characteristic data
		# we will use this data in the logging process within the Logger module, generating the alerts

		return alert

	'''

	'''
	def get_model_data(self, data_file):
		with open(data_file) as data_file:
			# Parse json data from the file
			model_data = json.load(data_file)

		return model_data

	'''
	
	'''
	def flow_feature_exclusion(self, flow):
		# Exclude features that do not get used in the prediction of the flow
		feature_vectors_to_keep = ['sTos','dTos','SrcWin','DstWin','sHops','dHops','sTtl',
		'dTtl','TcpRtt','SynAck','AckDat','SrcPkts','DstPkts','SrcBytes','DstBytes','SAppBytes',
		'DAppBytes','Dur','TotPkts','TotBytes','TotAppByte','Rate','SrcRate','DstRate']

 		# Only return the flow DataFrame features that match those defined in the required string
		feature_excluded_flow = flow.loc[:, feature_vectors_to_keep]

		return feature_excluded_flow