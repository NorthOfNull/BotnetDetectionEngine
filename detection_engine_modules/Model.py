import pickle

from sklearn.ensemble import RandomForestClassifier

'''

'''
class Model:
	'''

	'''
	def __init__(self, model_directory, model_file_name, model_metadata):
		self.model_object = None
		self.model_metadata = model_metadata
		self.model_file_name = model_file_name
		self.rel_model_file_path = model_directory + '/' + self.model_file_name


		self.load_model()

		print("[ Model ] Loaded", self.model_file_name)
		#print("[ Model ] Model Data =", self.model_metadata)


	'''

	'''
	def __del__(self):
		print("Deleting Model object -", self.model_file_name)


	'''	
	Opens the model file and de-serialises the pickeled object data.
	'''
	def load_model(self):
		with open(self.rel_model_file_path, 'rb') as model_file:
			self.model_object = pickle.load(model_file) 

		return 0


	'''	
	Gets the model's specific data from the json data file.
	'''
	def get_data(self):
		

		return 0

	'''

	'''
	def predict(self, flow):


		return labelled_flow