// log.js


// Handles adding flow_array data as rows in the flowLogTable
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

//
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
