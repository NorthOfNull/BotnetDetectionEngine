import unittest


from detection_engine_modules.Model import Model
from detection_engine_modules.Detector import Detector

#
# Model module testing file.
#

# Black box testing
class bb_ModelTest(unittest.TestCase):
    # __init__
    def test_init(self):
        '''
        Testing Model object initialisation.
        Input - Valid object init arguments.
        Requires - Nothing.
        Expected output - Successfully instantiate a Model object.
        '''
        model = Model('Models', 'Neris(1).model', 'test_metadata', True)

        self.assertTrue(model)




# White box testing
class wb_ModelTest(unittest.TestCase):
    # __init__
    def test_init__with_valid_args(self):
        '''
        Test to ensure that the model's init variables are correctly stored.
        Input - Valid object init arguments.
        Required - Metadata for the model, from the model_metadata file.
        Expected ouput - Successful model object returned and model details stored correctly.
        '''
        args = {'no_gui':True,
                'no_log':True,
                'debug':True,
                'read':'testing/testing_alerts.binetflow'}

        detector = Detector(args)
        metadata = detector.get_model_data(data_file_path='Models/model_data.json')
        
        model_name = 'Neris(1).model'
        metadata = metadata[model_name]

        model = Model('Models', model_name, metadata, True)

        self.assertTrue(model.model_object)
        self.assertEqual(model.model_metadata, metadata)
        self.assertEqual(model.model_file_name, 'Neris(1).model')
        self.assertEqual(model.rel_model_file_path, 'Models/Neris(1).model')
        self.assertTrue(model.loading_status)


    # load_model
    def test_load_model__with_invalid_args(self):
        '''
        Testing Model object's file loading function, with invalid args.
        Input - Nothing.
        Requires - Invalid object init arguments.
        Expected output - Model's loading_status variable to be false.
        '''
        model = Model('Not_a_directory', 'not.a.model', 'test_metadata', True)

        self.assertFalse(model.loading_status)
