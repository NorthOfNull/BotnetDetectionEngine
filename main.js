// Modules to control application life and create native browser window
const {app, BrowserWindow, ipcMain} = require('electron');
const path = require('path');
const WebSocket = require('ws');
const Data_Controller = require('./js/Data_Controller');

// Keep a global reference of the window object, if you don't, the window will
// be closed automatically when the JavaScript object is garbage collected.
let mainWindow;


function createWindow () {
    // Create the browser window.
    mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            contextIsolation: true, 
            preload: path.join(__dirname, 'js/preload.js')
        }
    })

    // and load the index.html of the app.
    mainWindow.loadFile('html/index.html');

    // Open the DevTools.
    // mainWindow.webContents.openDevTools()

    // Emitted when the window is closed.
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
    console.log("WS client connection established!");

    // Send data received on websocket from detection engine to the Data_Controller
    ws.on('message', function incoming(message) {
        dc.add_flow(message);
    });


    // Send data from data_controller from client to renderer process
    // Send to the ipcRenderer's 'fromMain' event
    ws.on('message', function incoming(message) {
        data = {
            'dcTotalFlows':dc.total_flow_count
        }

        mainWindow.webContents.send("fromMain", data);

        console.log('received: %s', message);
    });
});

// Listener for send functions from renderer process
ipcRenderer.on('toMain', function(event, fromPage) {
    if(fromPage == 'Dashboard') {
        
    }
});