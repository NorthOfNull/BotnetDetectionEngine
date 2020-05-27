"""
The Model Module.
"""

import pickle

from sklearn.ensemble import RandomForestClassifier

class Model:
    """
    The Model class handles the deserialised model objects.

    The Model objects must be instantated with the directory that the models are stored in, the model file name and it's metadata.

    Predictions on the status of the DataFrame can then be made. 
    """
    def __init__(self, model_directory, model_file_name, model_metadata, debug):
        """
        Constructor for the Model objects.

        Takes in a directory name, model file, name, and the model's data. This is retrieved and inputted from the Detector object.

        Args:
            model_directory (string): The name of the directory that the models are stored in.
            model_file_name (string): The name of the model file that is to be loaded.
            model_metadata (json-formatted string): The model's related metadata.

        Attributes:
            model_object (None or :obj:'RandomForestClassifier object'): The variable in which the deserialised model is stored.
            model_metadata (json-formatted string): The model's related metadata.
            model_file_name (string): The name of the model file that is to be loaded.
            rel_model_file_path (string): The full relative path for the model file.
        """
        self.model_object = None
        self.model_metadata = model_metadata
        self.model_file_name = model_file_name
        self.rel_model_file_path = model_directory + '/' + self.model_file_name

        self.debug = debug

        self.loading_status = self.load_model()

    def __del__(self):
        """
        The Model object's destructor.
        """
        #print("Deleting Model object -", self.model_file_name)
        return 0

    def load_model(self):
        """
        Opens the model file and de-serialises the pickeled object data into the model object's storage variable.

        Returns:
            loading_status (bool): The status of the model's deserialisation.
        """
        try:
            with open(self.rel_model_file_path, 'rb') as model_file:
                self.model_object = pickle.load(model_file)

                loading_status = True

                if(self.debug == True):
                    print("[ Model ] Loaded", self.model_file_name)
                    print("[ Model ] Model Data =", self.model_metadata)
        except:
            # Soft exception handling
            loading_status = False

            print("[ Model ] Model loading error -", self.model_file_name)

        return loading_status

    def predict(self, flow):
        """
        Makes a prediction, against the deserialised loaded model in memory, on the flow data to determine the data's label.

        Args:
            flow (:obj:'DataFrame'): The processed network flow DataFrame which it to be predicted on.

        Returns:
            prediction (string): The prediction, either 'Normal' or 'Botnet', depending on the model's prediction result from the inputted data.
        """
        # Make a prediction with the model object as to the classificaiton of the flow
        prediction = self.model_object.predict(flow)

        if(self.debug == True):
            print("[ Model ] Prediction from", self.model_file_name, " =", prediction)

        return prediction
