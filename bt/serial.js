#! /usr/bin/env node

var serialport = require("serialport");
var SerialPort = serialport.SerialPort;

var listPorts = function () {
  console.log("Available ports:\n");
  // list serial ports:
  serialport.list(function (err, ports) {
    ports.forEach(function(port) {
      console.log(port.comName);
    });
  });
};

var initPort = function (portName) {
  if (!portName) {
    throw new Error("Undefined port\n");
  }

  var port = new SerialPort(portName, {
    baudRate: 115200,
    parser: serialport.parsers.readline("\r\n")
  });

  function showPortOpen() {
    console.log('port open. Data rate: ' + port.options.baudRate);
  }

  function saveLatestData(data) {
    console.log(data);
  }

  function showPortClose() {
    console.log('port closed.');
  }

  function showError(error) {
    console.log('Serial port error: ' + error);
  }

  port.on('open', showPortOpen);
  port.on('data', saveLatestData);
  port.on('close', showPortClose);
  port.on('error', showError);
};

var showHelp = function () {
  var help = "Available commands:\n\nlist\nwrite <path>\nlisten <path>\n\n";
  console.log(help);
};

switch (process.argv[2]) {
  case "list":
    listPorts();
    break;
  case "listen":
    initPort(process.argv[3]);
    break;
  default:
    showHelp();
    break;
}
