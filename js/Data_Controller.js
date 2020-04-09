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


	// Add labelled_flow and alert _ata to the data_controller object's json object for storage
	add_data(flow) {

		// TODO
		// ADD DATA CHECKING AND PARSING TO JSON?


		// Exclude the csv header line from the flow data
		// (We do not include this line in Data_Controller's storage)
		if(!flow.match(/SrcAddr/gi)) {
			// if(flow's label == Botnet) { this.bot_flow_count += 1 }
			// if(flow's label == Botnet) { this.bot_flow_count += 1 }
			// if(flow's label == Botnet) { this.bot_flow_count += 1 }



			this.received_flows[this.total_flow_count] = flow;
			this.total_flow_count += 1;
		}
	}

	// Returns all stored flow data
	get_data() {
		let data = {
        	'dcTotalFlows':this.total_flow_count,
        	'dcBotFlows':this.bot_flow_count,
        	'dcReceivedFlows':this.received_flows
    	};

		return data;
	}
}
module.exports = Data_Controller;