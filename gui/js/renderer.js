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


// On data_controller object updates, received from main
window.api.receive("fromMain", (data) => {
    //console.log(data);

    if(data === null) {
    	return 0;
    }

    let page = document.getElementsByTagName("title")[0].innerHTML;

    // Home page rendering
    if(page == "Home") {
    	// Home Dashboard Rendering
    	let botFlowsData = document.getElementById("botFlowsData");
    	let totalFlowsData = document.getElementById("totalFlowsData");
        let botsTable = document.getElementById("botsTable");
        
        // Get data for the relevant fields
    	botFlowsData.innerHTML = data["dcBotFlows"];
    	totalFlowsData.innerHTML = data["dcTotalFlows"];

        if(data["dcBotFlows"] > 0) {
            botFlowsData.style.color = "red";
        }

        // If there are new alerts, update botsTable data
        if(data["dcReceivedAlerts"]) {
            add_bot_data(data['dcReceivedAlerts'], botsTable);
        }



    // Alerts page rendering
    } else if(page == "Alerts") {
        let alertsContainer = document.getElementById("alertsContainer");

        // Handling alertsContainer data
        if(data["dcReceivedAlerts"]) {
            let displayed_index = data["dcBotFlows"];

            if(Array.isArray(data["dcReceivedAlerts"])) {
                // Page load
                // Remove any existing content
                alertsContainer.innerHTML = "";

                for(alert in data["dcReceivedAlerts"]) {
                    let this_id = Number((displayed_index - data["dcReceivedAlerts"].length ) + alert) + 1;

                    alertsContainer.innerHTML += "<div class='alert' id=" + this_id + ">";

                    add_alert_item(data["dcReceivedAlerts"][alert], this_id);

                    alertsContainer.innerHTML += "</div>";
                }
            } else {
                // Append single alert item
                alertsContainer.innerHTML += "<div class='alert' id=" + displayed_index + ">";

                add_alert_item(data["dcReceivedAlerts"], displayed_index);

                alertsContainer.innerHTML += "</div>";

            }
        }


    // Activity Graph page rendering
    } else if(page == "Activity Graph") {
        // Counts number of normal and bot flows in a TIME PERIOD
        // If time period exceeds update time threshold, then plot the values 


    // Network Flow Log page rendering
    } else if(page == "Network Flow Log") {
    	// Flow Log Rendering
    	let flowLogTable = document.getElementById("flowLogTable");

        // Flow data
    	let flow_array = data["dcReceivedFlows"];

        flowLogTable.innerHTML = "";

        // Add table headings to the flowLogTable
        let table_headings = 'SrcAddr,DstAddr,Proto,Sport,Dport,State,sTos,dTos,SrcWin,DstWin,sHops,dHops,StartTime,LastTime,sTtl,dTtl,TcpRtt,SynAck,AckDat,SrcPkts,DstPkts,SrcBytes,DstBytes,SAppBytes,DAppBytes,Dur,TotPkts,TotBytes,TotAppByte,Rate,SrcRate,DstRate,Label';
        table_headings = table_headings.split(',');

        // Add table headings
        let heading_elements = "";

        for(col in table_headings) {
            let heading = table_headings[col];
            heading_elements += "<th>" + heading + "</th>"; 
        }

        flowLogTable.innerHTML += "<tr>" + heading_elements + "</tr>";
        
        // Add flow rows to table
        add_flow_rows(flow_array, flowLogTable);
    }
});
