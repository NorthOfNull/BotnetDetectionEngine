'''

'''

import os
import sys
import json
import pandas as pd

from detection_engine_modules.Model import Model
from detection_engine_modules.Logger import Logger
from detection_engine_modules.Sniffer import Sniffer
from detection_engine_modules.Websocket_Client import Websocket_Client


class Detector:
    '''

    '''
    def __init__(self, args):
        self.gui = args['no_gui']
        self.logging = args['no_log']
        self.debug = args['debug']
        self.read = args['read']

        self.dataset_feature_columns = ['SrcAddr', 'DstAddr', 'Proto', 'Sport', 'Dport', 'State',
                                        'sTos', 'dTos', 'SrcWin', 'DstWin', 'sHops', 'dHops',
                                        'StartTime', 'LastTime', 'sTtl', 'dTtl', 'TcpRtt', 'SynAck',
                                        'AckDat', 'SrcPkts', 'DstPkts', 'SrcBytes', 'DstBytes',
                                        'SAppBytes', 'DAppBytes', 'Dur', 'TotPkts', 'TotBytes',
                                        'TotAppByte', 'Rate', 'SrcRate', 'DstRate']

        self.models = []
        self.model_directory = 'Models'
        self.socket_addr = "ws://localhost:5566"


        if self.debug:
            print("[ Detector ] Debugging output enabled.")

        # De-serialise model objects into the model array
        self.models = self.load_models()

        # Sniffs raw data from a SPAN'd port, performs netflow feature extraction.
        # Mimics bash shell behaviour of:
        # $ TCPDUMP (interface) | ARGUS | RA CLIENT (CSV Formatted Network Flow Exporter).
        # Or, reads from a given file
        self.sniffer = Sniffer(self.read)

        if(self.gui == True):
            # Websocket_Client instantiation
            # Faciliates data transfer through a localhost socket to the backend electron
            # nodejs server
            self.ws_client = Websocket_Client()

            # And attempt to create a connection to the websocker server
            self.ws_client.connect(self.socket_addr)

        if(self.logging == True):
            # Flow and Alert file logging
            # Initialise Logger instance to handle alert and flow file logging operations
            self.logger = Logger()

    '''

    '''
    def __del__(self):
        if(self.debug == True):
            print("Deleting Detector object and the loaded models.")


    '''
    Main running loop for the detector.

    Gets flows from the network flow sniffer, predicts the behaviour via the models 
    and outputs the data.
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

            # Get raw flow string from the sniffer instance.
            # Gets flow data from the a processed .pcap file, .binetflow csv file or from the
            # network interface.
            flow_string = self.sniffer.get_flow()

            if flow_string != False:
                # Process the flow_string into a DataFrame with the required feature vectors
                # being maintained,
                # So that the flow data is ready to make predictions
                flow = self.process_flow(flow_string)

                # If there is a valid flow (i.e. self.process_flow successfully returns
                # a processed_flow)
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


                # If gui is enabled
                if(self.gui == True):
                    # Send the flow and any alert data to the gui instance, via the websocket
                    self.ws_client.send(labelled_flow, alert)

                # If logging is enabled
                if(self.logging == True):
                    # Log the labelled flow output to the file
                    self.logger.write_flow_to_file(labelled_flow)

                    if(alert != None):
                        # If ther is an alert, we log it to file
                        self.logger.write_alert_to_file(alert)
            else:
                # No further flows received from the sniffer.
                # Exit main running loop
                break

        return 0

    '''
    De-serialisation of trained Machine Learning models that are contained in the
    'Models' directory.
    
    Loaded objects get stored in the 'self.models' array, along with their descriptive data.

    '''
    def load_models(self):
        models = []
        model_data = None

        if(self.debug):
            print("[ Detector ] Loading Models...")

        # Handle nothing being present in directory
        # Handle directory not being present
        assert(os.path.exists(self.model_directory))

        # Get model metadata from the json file
        data_file_path = self.model_directory + '/model_data.json'
        model_json_metadata = self.get_model_data(data_file_path)


        # Load models that have file names present within the model_json_metadata file
        # (filenames are stored as the json keys)
        for model_file_name in model_json_metadata.keys():
            # Get the model's data
            model_data = model_json_metadata[model_file_name]

            # Instantiate model object, with the full relative directory path, model file name and
            # it's metadata being passed as an argument.
            instance_of_model = Model(self.model_directory, model_file_name, model_data, self.debug)

            if(instance_of_model.loading_status == True):
                # If the model is succesfully loaded
                # Add the model object to the Detector
                models.append(instance_of_model)
            else:
                # Object cleanup
                del instance_of_model


        print("[ Detector ] Loaded", len(models), "/", len(model_json_metadata.keys()), "models.")

        if(len(models) == 0):
            print("[ Detector ] No valid models found to load.")
            sys.exit()

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

            # If the last field is empty
            if(flow[-1] == ''):
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
        # Required to only pass valid the model feature vector (the features that the models were
        # trained on) to the models, ready for prediction
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

            # And generate an alert, filled with relevant flow data and the exhibited botnet-like
            # characteristics of the traffic
            alert = self.generate_alert(original_flow, prediction, predicted_model_data)
        else:
            prediction = 'Normal'


        if(self.debug and prediction == 'Botnet'):
            print("[ debug ] Overall prediction =", prediction)
            print("[ debug ] Alert:\n", alert)


        return prediction, alert

    '''
    Generates an alert json data structure from the specific data of each positive prediction model.

    @returns The generated alert data in json format.
    '''
    def generate_alert(self, flow, prediction, predicted_model_data):
        if(self.debug == True):
            print("[ Detector ] Botnet flow found. Generating alert...")

        # If flow is botnet, we generate the alert
        # Construction is implemented via getting data from the flow
        # And also data from the models that predicted that particular behaviour
        if(prediction == 'Botnet'):
            # Get flow data
            # Source data
            src_addr = flow['SrcAddr'].item()
            s_port = flow['Sport'].item()

            # Destination data
            dst_addr = flow['DstAddr'].item()
            d_port = flow['Dport'].item()

            # Protocol data
            proto = flow['Proto'].item()

            # Date-time and duration data
            start_time = flow['StartTime'].item()
            dur = flow['Dur'].item()


            # Get predicted model data
            bots = []
            comms_protocl = []
            activity = []

            for data in predicted_model_data:
                # Add unique instances the data categories for each predicted_model_data instance
                # Bot name data
                bot_name = data['Bot']

                if bot_name not in bots:
                    bots.append(bot_name)

                # Bot comms_protocl data
                bot_comm_protocol = data['Communication Protocol']

                if bot_comm_protocol not in comms_protocl:
                    comms_protocl.append(bot_comm_protocol)

                # Bot Activity data
                bot_activity = data['Activity']

                # Handles the presence of more than one activity characteristic
                for activity_item in bot_activity:
                    if activity_item not in activity:
                        activity.append(activity_item)


        # Generate json alert
        # First create the alert data
        alert = {"Src": {"Addr": src_addr,
                         "Port": s_port},
                 "Dst": {"Addr": dst_addr,
                         "Port": d_port},
                 "Proto": proto,
                 "Time":{"StartTime": start_time,
                         "Dur": dur},
                 "Bots": bots,
                 "Comms_protocol": comms_protocl,
                 "Activity": activity
                }


        return alert

    '''

    '''
    def get_model_data(self, data_file_path):
        with open(data_file_path) as data_file:
            try:
                # Parse json data from the file
                model_data = json.load(data_file)
            except:
                # No exception - hard exit.
                print("[ Detector ] 'Model_data.json' file read error.")
                sys.exit()

        return model_data

    '''
    
    '''
    def flow_feature_exclusion(self, flow):
        # Exclude features that do not get used in the prediction of the flow
        feature_vectors_to_keep = ['sTos', 'dTos', 'SrcWin', 'DstWin', 'sHops', 'dHops', 'sTtl',
                                   'dTtl', 'TcpRtt', 'SynAck', 'AckDat', 'SrcPkts', 'DstPkts',
                                   'SrcBytes', 'DstBytes', 'SAppBytes', 'DAppBytes', 'Dur',
                                   'TotPkts', 'TotBytes', 'TotAppByte', 'Rate', 'SrcRate',
                                   'DstRate']

        # Only return the flow DataFrame features that match those defined in the required string
        feature_excluded_flow = flow.loc[:, feature_vectors_to_keep]

        return feature_excluded_flow
