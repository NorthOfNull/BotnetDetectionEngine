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

// Adds single row
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


// Add flowLogTable headers on page load
document.addEventListener('DOMContentLoaded', function() {
    let flowLogTable = document.getElementById("flowLogTable");

    // Page load
    // Format table headings string into split array
    let table_headings = 'SrcAddr,DstAddr,Proto,Sport,Dport,State,sTos,dTos,SrcWin,DstWin,sHops,dHops,StartTime,LastTime,sTtl,dTtl,TcpRtt,SynAck,AckDat,SrcPkts,DstPkts,SrcBytes,DstBytes,SAppBytes,DAppBytes,Dur,TotPkts,TotBytes,TotAppByte,Rate,SrcRate,DstRate,Label';
    table_headings = table_headings.split(',');

    // Add table headings
    let heading_elements = "";

    for(col in table_headings) {
        let heading = table_headings[col];
        heading_elements += "<th>" + heading + "</th>"; 
    }

    flowLogTable.innerHTML += "<tr>" + heading_elements + "</tr>";
});