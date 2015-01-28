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

stdin.addListener("data", function(d) {
  var input = d.toString().substring(0, d.length-1);
  switch (input) {
    case 1:
      lastCommand = "goForward";
      break;
    case 2:
      lastCommand = "goBackward";
      break;
    default:
      lastCommand = "stop";
      break;
  }
});

port.on('open', function () {
  console.log('port open. rate: ', port.options.baudRate);
});

port.on('data', function (data) {
  console.log('received:', data.toString());
  port.write(new Buffer(lastCommand, 'utf-8'), function(err) {
    if (err) {
      console.log('err ' + err);
    }
  });
});

port.on('close', function () {
  console.log('in port closed.');
});

port.on('error', function (err) {
  console.log('in port error.', err);
});
