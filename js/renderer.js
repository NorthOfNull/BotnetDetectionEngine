// This file is required by the index.html file and will
// be executed in the renderer process for that window.
// No Node.js APIs are available in this process because
// `nodeIntegration` is turned off. Use `preload.js` to
// selectively enable features needed in the rendering
// process.


// Inital page rendering 
// TODO
// SEND REQUEST TO MAIN.JS IPCRENDERER LISTENER
// AND GET INITAL DATA TO DISPLAY AT PAGE LOAD


// On data_controller object updates
window.api.receive("fromMain", (data) => {
    console.log(data);


    let page = document.getElementsByTagName("title")[0].innerHTML;

    if(page == "Dashboard") {
    	// Dashboard Rendering
    	let totalFlowData = document.getElementById("totalFlowsData");

    	totalFlowData.innerHTML = data["dcTotalFlows"]

    } else if(page == "Flow Log") {
    	// Flow Log Rendering
    	let flowLogTable = document.getElementById("flowLogTable");

    	console.log("FLOWWWWWWWWWWWW")
    }
});