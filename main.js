// Modules to control application life and create native browser window
const { app, BrowserWindow, ipcMain } = require('electron');

const path = require('path');
const WebSocket = require('ws');
const Data_Controller = require('./gui/js/Data_Controller');


// Keep a global reference of the window object, if you don't, the window will
// be closed automatically when the JavaScript object is garbage collected.
let mainWindow;

function createWindow () {
    // Create the browser window.
    mainWindow = new BrowserWindow({
        width: 1500,
        height: 900,
        darkTheme: true,
        webPreferences: {
            contextIsolation: true, 
            preload: path.join(__dirname, 'gui/js/preload.js')
        }
    })

    // and load the index.html of the app
    mainWindow.loadFile('gui/html/index.html');

    // Open the DevTools
    mainWindow.webContents.openDevTools()

    // Set localStorage default state for navbar on creation of the window
    mainWindow.webContents.executeJavaScript('localStorage.setItem("navbar", "closed");')

    // Emitted when the window is closed
    mainWindow.on('closed', function () {
        // Dereference the window object, usually you would store windows
        // in an array if your app supports multi windows, this is the time
        // when you should delete the corresponding element.
        mainWindow = null;
    })
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', createWindow);

// Quit when all windows are closed.
app.on('window-all-closed', function () {
    // On macOS it is common for applications and their menu bar
    // to stay active until the user quits explicitly with Cmd + Q
    if (process.platform !== 'darwin') app.quit();
});




// Create data_controller object on window creation
// Allows global data control 
// Pages can request data from this object via ipcRenderer control
let dc = new Data_Controller();


// WebSocket Server 
// Receives labelled flows from the Botnet Detection Engine
const wss = new WebSocket.Server({ port: 5566 });

// Handle connection event from a websocket client 
wss.on('connection', function connection(ws) {
    console.log("[ Electron ] WS client connection established!");


    // Send data from data_controller from client to renderer process
    // Send to the ipcRenderer's 'fromMain' event
    ws.on('message', function incoming(message) {
        // Add the flow and alert data to the Data_Controller instance
        parsed_data = dc.add_data(message);

        // Get data to send
        let data = dc.get_all_data();

        // Send updated data_controller data to the renderer instance
        send_data(data);

    });
});


// Listener for data requests from the renderer process
// Sends all data stored within the Data_Controller instance
ipcMain.on('toMain', function(event, request) {
    if(request == 'init_data') {
        // Get data to send
        let data = dc.get_all_data();

        send_data(data);
    }
});


// Sends new data to the renderer process
function send_data(data=false) {
    if(data == false) {
        console.log("Error - No Data to send from <send_data>");
    }

    // Send data to the renderer process
    mainWindow.webContents.send("fromMain", data);
}