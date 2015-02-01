#! /usr/bin/env node

var serialport = require("serialport");
var SerialPort = serialport.SerialPort;

var portName = "/dev/cu.Bluetooth-Incoming-Port";
var port = new SerialPort(portName, {
  baudRate: 115200
});
var sys = require("sys");
var stdin = process.openStdin();

var lastCommand = "stop";
var portOpen = false;

stdin.addListener("data", function(d) {
  var input = d.toString().substring(0, d.length-1);
  switch (input) {
    case "1":
      lastCommand = "run";
      break;
    case "2":
      lastCommand = "goForward";
      break;
    case "3":
      lastCommand = "goBackward";
      break;
    default:
      lastCommand = "stop";
      break;
  }
  console.log("your command:", lastCommand);
  if (portOpen) port.write(new Buffer(lastCommand + '\r\n', 'utf-8'), function(err) {
    if (err) {
      console.log('err ' + err);
    }
  });
});

port.on('open', function () {
  portOpen = true;
  console.log('port open. rate: ', port.options.baudRate);
});

port.on('data', function (data) {
  console.log('received:', data.toString());
});

port.on('close', function () {
  portOpen = false;
  console.log('in port closed.');
});

port.on('error', function (err) {
  portOpen = false;
  console.log('in port error.', err);
});
