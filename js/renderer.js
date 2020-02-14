// This file is required by the index.html file and will
// be executed in the renderer process for that window.
// No Node.js APIs are available in this process because
// `nodeIntegration` is turned off. Use `preload.js` to
// selectively enable features needed in the rendering
// process.
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