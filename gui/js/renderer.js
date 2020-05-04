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
        if(data["dcReceivedAlerts"].length != 0) {
            add_bot_data(data['dcReceivedAlerts'], botsTable);
        }



    // Alerts page rendering
    } else if(page == "Alerts") {
        let alertsContainer = document.getElementById("alertsContainer");

        // Remove all elements
        alertsContainer.innerHTML = "";

        // Handling alertsContainer data
        if(data["dcReceivedAlerts"] != null) {
            // Render all alert items if more than one alert is present in the received data
            for(index in data["dcReceivedAlerts"]) {
                add_alert_item(data["dcReceivedAlerts"][index], alertsContainer);
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

// Finds the unique bot IP's from the alerts and counts the instances for each IP
function add_bot_data(data, botsTable) {
    let uniqueBotIPs = {};

    botsTable.innerHTML = "";

    for(alert in data) {
        // Get Bot source IP address
        botIP = data[alert]['Src']['Addr'];

        // Checking if botIP is already in uniqueBotIPs
        if(Object.keys(uniqueBotIPs).indexOf(botIP) == -1) {
            // Add unique IP
            uniqueBotIPs[botIP] = 1;
        } else {
            // IP already in unique IP's
            // Increment instance count
            uniqueBotIPs[botIP] += 1;
        }
    }

    botsTable.innerHTML += "<tr><th>Bot IP</th><th>Flow Count</th></tr>";

    // Add data to botsTable
    for(bot in uniqueBotIPs) {
        botsTable.innerHTML += "<tr><td>" + bot + "</td>" + "\n<td>" + uniqueBotIPs[bot] + "</td></tr>";
    }

    return 0;
}


function add_alert_item(data, alertsContainer) {
    let displayed_index = (alertsContainer.childElementCount / 10) + 1;

    // Start button element
    alertsContainer.innerHTML += "<button type='Button' class='collapse'>Alert #" + displayed_index + "</button>"

    // Start alert_item div
    alertsContainer.innerHTML += "<div class='alert_item'>";

    // Get alert data keys values into a data string array
    data_string = [
            "Source = " + data.Src['Addr'] +  ":" + data.Src['Port'],
            "Destination = " + data.Dst['Addr'] + ":" + data.Dst['Port'],
            "Protocol = " + data['Proto'],
            "DateTime = " + data.Time['StartTime'],
            "Flow Duration = " + data.Time['Dur'] + " seconds",
            "Bots = " + data['Bots'],
            "Comms_protocol = " + data['Comms_protocol'],
            "Activity = " + data['Activity']
    ]

    for(row in data_string) {
        alertsContainer.innerHTML += "<p>" + data_string[row] + "</p>";
    }

    // Close alert_item div
    alertsContainer.innerHTML += "</div>";

    return 0;
}

function add_flow_rows(flow_array, flowLogTable) {
    // Dynamically network flow rows to the flowLogTable
    // For each flow in the flow_array data, we add a row
    for(index in flow_array) {
        // Get flow from array's index
        let flow = flow_array[index];

        // Add the as a flow row
        add_row(flow, flowLogTable);
    }

    return 0;
}

function add_row(flow, flowLogTable) {
    // Handles adding a single flow to the a single row
    // Split string
    flow = flow.split(',');

    let row_data_elements = "";

    // Checks if flow is labelled botent
    let flow_label = flow[flow.length - 1];

    // Add data from each index of the flow to the table row data elements
    for(col in flow) {
        let data = flow[col];

        // If botnet flow present, style with red font colour
        if(flow_label == "Botnet") {
            row_data_elements += "<td style=\"color:red;\">" + data + "</td>";
        } else {
            row_data_elements += "<td>" + data + "</td>";
        }
    }

    flowLogTable.innerHTML += "<tr>" + row_data_elements + "</tr>";

    return 0;
}

