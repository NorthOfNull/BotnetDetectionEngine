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

            if(data["dcReceivedAlerts"].length > 1) {
                // Page load
                // Remove any existing content
                alertsContainer.innerHTML = "";

                for(alert in data["dcReceivedAlerts"]) {
                    let this_id = Number(alert) + 1;

                    alertsContainer.innerHTML += "<div class='alert' id=" + this_id + ">";

                    add_alert_item(data["dcReceivedAlerts"][alert], this_id);

                    alertsContainer.innerHTML += "</div>";
                }
            } else if(data["dcReceivedAlerts"] != ''){
                if(document.getElementById("no_alert_text")) {
                    alertsContainer.innerHTML = "";
                }

                // Append single alert item
                alertsContainer.innerHTML += "<div class='alert' id=" + displayed_index + ">";

                add_alert_item(data["dcReceivedAlerts"], displayed_index);

                alertsContainer.innerHTML += "</div>";
            }
        }


    // Activity Graph page rendering
    } else if(page == "Activity Graph") {
        // We only want to push updates, so we do not update on page load
        // (which forces all data from Data_Controller to be sent as an array)
        if(!Array.isArray(data["dcReceivedFlows"])) {
            // Must ensure that the correct counts are incremented
            // So, we find if there has been an alert (for the bot count) and a received flow (for the flow count) 
            increment_bot_count = false;
            increment_flow_count = false;

            if(data["dcReceivedAlerts"]) {
                increment_bot_count = true;
            }

            if(data["dcReceivedFlows"].length > 0) {
                increment_flow_count = true;
            }

            update_interval_counts(increment_bot_count, increment_flow_count);
        }



    // Network Flow Log page rendering
    } else if(page == "Network Flow Log") {
        // Flow Log Rendering
        let flowLogTable = document.getElementById("flowLogTable");

        console.log(typeof(data["dcReceivedFlows"]))

        if(data["dcReceivedFlows"]) {
            // Handle data input type
            if(typeof(data["dcReceivedFlows"]) != 'string') {
                // Call function to handle array of flows and add each row seperately
                add_flow_rows(data["dcReceivedFlows"], flowLogTable);
            } else if(typeof(data["dcReceivedFlows"]) == 'string'){
                // Call function to add a single row
                add_row(data["dcReceivedFlows"], flowLogTable);
            }
        }
    }
});
