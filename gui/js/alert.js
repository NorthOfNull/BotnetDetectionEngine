// alert.js

// Updates the alerts to the alert_box
function add_alert_item(data, index) {
    // Get the alert div id
    alert_box = document.getElementById(index);

    // Start button element
    alert_box.innerHTML += "<button type='Button' class='collapse' onclick=toggle_alert(" + index + ")>Alert #" + index + "<img src='../icons/dropdown_icon.png'></img>" + "</button>";

    // Get alert data keys values into a data string array
    data_string = [
            ["Source = ", data.Src['Addr'] +  ":" + data.Src['Port']],
            ["Destination = ", data.Dst['Addr'] + ":" + data.Dst['Port']],
            ["Protocol = ", data['Proto']],
            ["DateTime = ", data.Time['StartTime']],
            ["Flow Duration = ", data.Time['Dur'] + " seconds"],
            ["Bots = ", data['Bots']],
            ["Comms_protocol = ", data['Comms_protocol']],
            ["Activity = ", data['Activity']]
    ]

    for(row in data_string) {
        alert_box.innerHTML += "<p>" + data_string[row][0] + data_string[row][1] + "</p>";
    }

    return 0;
}

// Toggles the icon rotation style and the display status of the alert data specified by the index id
function toggle_alert(index) {
    alert_item = document.getElementById(index);

    // Toggle icon rotation and display status of alert data
    icon = alert_item.getElementsByTagName("img");
    alert_data = alert_item.getElementsByTagName("p");

    current_state = icon[0].style.transform;

    if(current_state == "rotateX(0deg)" || current_state == "") {
        // Icon
        icon[0].style.transform = "rotateX(180deg)";

        // Alert data
        alert_item.style.height = "300px";

        for(let i = 0; i < alert_data.length; i++) {
            alert_data[i].style.display = "block";
        }
    } else {
        // Icon
        icon[0].style.transform = "rotateX(0deg)";

        // Alert data
        alert_item.style.height = "30px";

        for(let i = 0; i < alert_data.length; i++) {
            alert_data[i].style.display = "none";
        }
    }

    return 0;
}
