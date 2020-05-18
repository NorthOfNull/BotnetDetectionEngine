// index.js

let uniqueBotIPs = {};

// Finds the unique bot IP's from the alerts and counts the instances for each IP
// And adds/updates the bot data into the botsTable
function add_bot_data(data, botsTable) {
    // Remove 'no bots' element message
    let no_bots_msg = document.getElementById("no_bots_msg").innerHTML = "";

    botsTable.innerHTML = "";

    if(Array.isArray(data)) {
        for(alert in data) {
            // Get Bot source IP address
            botIP = data[alert]['Src']['Addr'];

            add_unique_bot_IP(botIP);
        }
    } else {
        // Get Bot source IP address
        botIP = data['Src']['Addr'];

        add_unique_bot_IP(botIP);
    }

    // Add header row
    botsTable.innerHTML += "<tr><th>Bot IP</th><th>Flow Count</th></tr>";


    // Add data to botsTable
    for(bot in uniqueBotIPs) {
        botsTable.innerHTML += "<tr><td>" + bot + "</td>" + "\n<td>" + uniqueBotIPs[bot] + "</td></tr>";
    }

    return 0;
}


// Adds the unique ip data to the dictionary
function add_unique_bot_IP(botIP) {
    // Checking if botIP is already in uniqueBotIPs
    if(Object.keys(uniqueBotIPs).indexOf(botIP) == -1) {
        // Add unique IP
        uniqueBotIPs[botIP] = 1;
    } else {
        // IP already in unique IP's
        // Increment instance count
        uniqueBotIPs[botIP] += 1;
    }

    return 0;
}