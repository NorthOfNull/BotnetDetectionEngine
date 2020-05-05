'''

'''

import pickle

from sklearn.ensemble import RandomForestClassifier

class Model:
    '''

    '''
    def __init__(self, model_directory, model_file_name, model_metadata, debug):
        self.model_object = None
        self.model_metadata = model_metadata
        self.model_file_name = model_file_name
        self.rel_model_file_path = model_directory + '/' + self.model_file_name

        self.debug = debug

        self.loading_status = self.load_model()

    '''

    '''
    def __del__(self):
        #print("Deleting Model object -", self.model_file_name)
        return 0

    '''
    Opens the model file and de-serialises the pickeled object data.
    '''
    def load_model(self):
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

    '''

    '''
    def predict(self, flow):
        # Make a prediction with the model object as to the classificaiton of the flow
        prediction = self.model_object.predict(flow)

        if(self.debug == True):
            print("[ Model ] Prediction from", self.model_file_name, " =", prediction)

        return prediction
