// activity_graph.js


// Data storage; accumulates on updates from the detector when the activity_graph page is loaded
let interval_bot_count = 0;
let interval_flow_count = 0;

// Update Interval (ms)
let update_interval = 1000;
let update_interval_slider = document.getElementById("update_interval_slider");
let update_interval_value = document.getElementById("update_interval_value");

// X-axis Display Limit
let x_axis_display_limit = 20;
let x_axis_slider = document.getElementById("x_limit");
let x_axis_value = document.getElementById("x_limit_value");

// Graph Canvas
let activity_graph_canvas = document.getElementById("activity_graph");

// Define chart object to occupy the 'actvity_graph_canvas'
let chart = new Chart(activity_graph_canvas, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            spanGaps: true,
            label: 'Bot Flows',
            data: [],
            backgroundColor: [
                'rgba(255, 20, 0, 0.6)'
            ],
            borderColor: [
                'rgba(255, 20, 0, 0.6)'
            ],
            fill: 'origin',
            borderWidth: 1
        },
        {
            spanGaps: true,
            label: 'Received Flows',
            data: [],
            backgroundColor: [
                'rgba(0, 0, 255, 0.4)'
            ],
            borderColor: [
                'rgba(0, 0, 255, 0.4)',
            ],
            fill: 'origin',
            borderWidth: 1
        }]
        
    },
    options: {
        legend: {
            labels: {
                fontColor: 'white'
            }
        },
        scales: {

            xAxes: [{
                ticks: {
                    fontColor: 'white'
                },
                gridLines: {
                    color: 'gray'
                }
            }],
            yAxes: [{
                ticks: {
                    beginAtZero: true,
                    stepValue: 5,
                    fontColor: 'white'
                },
                gridLines: {
                    color: 'gray'
                }
            }]
        },
        animation: {
            easing: 'linear',
            duration: update_interval
        }
    }
});

// Increments  count values to latest
function update_interval_counts(increment_bot_count, increment_flow_count) {
    if(increment_bot_count) interval_bot_count++;
    if(increment_flow_count) interval_flow_count++;

    return 0;
}

// Handle the updating of chart data, called at a set interval
// Also calls 'reset_interval_counts'
function update_chart() {
    // Ensure X-Axis displays a maximum of x_axis_display_limit data points
    limit_x_axis_display()

    


    // Add new interval data to the chart object's datasets
    chart.data.datasets[0]['data'].push(interval_bot_count);
    chart.data.datasets[1]['data'].push(interval_flow_count);

    // Add new xAxes time label to chart object
    let date = new Date();
    let time = date.getHours() + ':' + date.getMinutes() + ':' + date.getSeconds();
    chart.data.labels.push(time);

    // Call update on chart object
    chart.update()


    // Reset interval count variables
    reset_interval_counts();

    // Set new update_interval with the slider value
    setTimeout(update_chart, update_interval);    

    return 0;
}


// Recursive function to limit x_axis data length
function limit_x_axis_display() {
    if(chart.data.labels.length >= x_axis_display_limit) {
        // If X-Axis length is too large, remove data from the x-axis label and data array first elements by shifting
        chart.data.labels.shift();
        chart.data.datasets[0]['data'].shift();
        chart.data.datasets[1]['data'].shift();

        // If the display limit is reduced between updates, recurse the display limiting and recheck
        if(chart.data.labels.length >= x_axis_display_limit) {
            limit_x_axis_display();
        }
    }

    return 0;
}


// Resets the data interval storage values to default
function reset_interval_counts() {
    interval_bot_count = 0;
    interval_flow_count = 0;

    return 0;
}


// Update Interval slider event handler
update_interval_slider.oninput = function() {
    // Set new display value
    update_interval_value.innerHTML = this.value;

    // Convert seconds to ms for update interval
    update_interval = this.value * 1000;
};

// X-Axis display limit slider event handler
x_axis_slider.oninput = function() {
    // Set new display value
    x_axis_value.innerHTML = this.value;

    // Update chart x-axis limit
    x_axis_display_limit = this.value;
};

// Update chart onload
chart.update()

// Set the interval at which the chart updates
setTimeout(update_chart, update_interval)