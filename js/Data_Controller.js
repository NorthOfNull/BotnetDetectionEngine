// Data Controller Module Class
// Handles data from the Botnet Detection Engine
class Data_Controller {
	constructor() {
		// JSON Object to hold received flows
		this.received_flows = [];

		// Integer counts of processed flows
		this.total_flow_count = 0;
		this.bot_flow_count = 0;
	}

	// Add flow to the data_controller object's json object for storage
	add_flow(flow) {

		// TODO
		// ADD DATA CHECKING AND PARSING TO JSON?

		this.received_flows[this.total_flow_count] = flow;

		this.total_flow_count += 1;
	}
}
module.exports = Data_Controller;