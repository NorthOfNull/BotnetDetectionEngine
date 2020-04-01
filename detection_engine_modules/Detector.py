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
from detection_engine_modules.Model import Model

'''

'''
class Detector:
	'''

	'''
	def __init__(self):
		self.model_directory = 'models/'
		self.models = []
		self.failed_loading_models = False

		self.load_models()


	'''

	'''
	def __del__(self):
		print("Deleting Detector object and the loaded models.")

		# TODO 
		# TODO
		# TODO
		# DELETE LOADED MODELS
		# del self.models


	'''
	De-serialisation of trained Machine Learning models that are contained in the 'Models' directory.
	Loaded objects get stored in the 'self.models' array, along with their descriptive data.

	'''
	def load_models(self):
		# Handle nothing being present in directory
		# Handle directory not being present
		if(os.path.exists(self.model_directory)):
			self.failed_loading_models = True
			print("FAILED LOADING MODELS")


		return 0


	'''
	Predicts the label of the given network flow data.
	If the flow is predicted as botnet, we return the data about the models that made the prediction.

	@returns The labelled network flow (csv format)
	@returns The model data, in the form of an alert, from positive models.
	'''
	def predict(self, flow):
		# Predict the label of the flow using each loaded model
		alert = None
		predicted_model_data = []


		# for model in self.models:
		#	prediction = model.predict(flow)
		#	
		#   labelled_flow = flow + prediction
		# 
		#   if(prediction == 'Botnet'):
		#		predicted_model_data.append(model.data) 
		#	



		# If a positive botnet prediction is made from one or more 
		# 
		# if(predictied_model_data):
		# 	alert = generate_alert(labelled_flow, predicted_model_data)


		# get 'bot_alert_data' from the model object's data that is loaded from the json file that stores model characteristic data
		# we will use this data in the logging process within the Logger module, generating the alerts

		return labelled_flow, alert


	'''
	Generates an alert data structure from the specific data of each positive prediction model.

	@returns The generated alert data
	'''
	def generate_alert(self, labelled_flow, predicted_model_data):
		print("!!!!!!!GENERATING ALERT!!!!!!!!")		

		# get 'predicted_model_data' from the model object's data that is loaded from the json file that stores model characteristic data
		# we will use this data in the logging process within the Logger module, generating the alerts

		return alert