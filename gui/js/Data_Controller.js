// Data Controller Module Class
// Handles data from the Botnet Detection Engine
class Data_Controller {
    constructor() {
        // JSON Object to hold received flows
        this.received_flows = [];
        this.received_alerts = [];

        // Integer counts of processed flows
        this.total_flow_count = 0;
        this.bot_flow_count = 0;
    }


    // Add labelled_flow and alert data to the data_controller object's json object for storage
    add_data(data) {
        // Parse the received JSON data
        data = JSON.parse(data) 

        // Extract the flow and alert data
        let flow = data['flow']
        let alert = data['alert']


        // Alert handling
        if(alert != null) {
            // If alert is present
            // Add alert to the storage array
            this.received_alerts[this.bot_flow_count] = alert

            // If there is an alert, then there is a botnet instance
            // Thus, the botnet instance counter is incremented
            this.bot_flow_count += 1;
        }
        
        // Flow handling
        // Exclude the csv header line from the flow data
        // (We do not include this line in Data_Controller's storage)
        if(!flow.match(/Label/gi)) {
            // Adding the received flow data
            this.received_flows[this.total_flow_count] = flow;

            // Incrementing total flow counter
            this.total_flow_count += 1;
        }

        return data;
    }


    // Returns all stored flow data
    get_all_data() {
        let data = {
            'dcTotalFlows':this.total_flow_count,
            'dcBotFlows':this.bot_flow_count,
            'dcReceivedFlows':this.received_flows,
            'dcReceivedAlerts':this.received_alerts
        };

        return data;
    }
}
module.exports = Data_Controller;