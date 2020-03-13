// This file is required by the index.html file and will
// be executed in the renderer process for that window.
// No Node.js APIs are available in this process because
// `nodeIntegration` is turned off. Use `preload.js` to
// selectively enable features needed in the rendering
// process.


// Inital page rendering 
// Sends request to the main process, requesting the data from the Data_Controller instance
// Essentially, forcing a message to be sent 'fromMain'
// This is to initialise the page's script with the relevant data available
window.api.send("toMain", "init_data");


// On data_controller object updates
window.api.receive("fromMain", (data) => {
    console.log(data);

    if(data === null) {
    	return 0;
    }

    let page = document.getElementsByTagName("title")[0].innerHTML;

    if(page == "Dashboard") {
    	// Dashboard Rendering
    	let botFlowsData = document.getElementById("botFlowsData");
    	let totalFlowsData = document.getElementById("totalFlowsData");

    	botFlowsData.innerHTML = data["dcBotFlows"];
    	totalFlowsData.innerHTML = data["dcTotalFlows"];



    } else if(page == "Flow Log") {
    	// Flow Log Rendering
    	let flowLogTable = document.getElementById("flowLogTable");

    	let flow_list = data["dcReceivedFlows"];

    	if(Array.isArray(data["dcReceivedFlows"])) {
    		let flow_array = data["dcReceivedFlows"];

    		console.log(typeof flow_array);

    		// TODO 
    		// HANDLE ARRAY TABLE ROW INSERTS 
    		// AND THEN THE DATA FOR EACH ONE

    		// for flow in flow_array:
    		//		add_flow_row(flow)
		
    	} else {
    		let flow = data["dcReceivedFlows"];

    		console.log(typeof flow);

    		// just need to do one add flow here
    		//
    		// add_flow_row(flow)
    	}


    	// TODO
    	// TODO
    	// TODO
    	// TODO
    	// SORT THIS RENDERER OUT FOR THE FLOW LOG PAGE
    	


    	// For loop handles instances of more than one flow in the data received
    	// i.e. in the case of init_data, where an array of flow data is generally sent from the 
    	// Data_Controller instance data storage
    	for(flow_csv in flow_list) {
    		// Split csv string into array elements
    		
    		// console.log(flow_csv[2]);

    		console.log(typeof flow_csv);


    		let flow = flow_csv.split(',');


    		// Insert the new row into the table
    		let row = flowLogTable.insertRow(-1);

    		// Create table data elements
    		let srcAddr = row.insertCell(0);
    		let dstAddr = row.insertCell(1);

    		// TODO 
    		// ADD MORE HERE
    		// PROBABLY ONLY THE RELEVENT FIELDS!!!! FILTER THE REQUIRED FIELDS BEFORE THE CREATION OF THE NEW ROW ON LINE 42?



    		// Add relevant data to the row's fields
    		srcAddr.innerHTML = flow[0];
    		dstAddr.innerHTML = flow[1];

    		// TODO 
    		// ADD MORE HERE
    	}
    }
});