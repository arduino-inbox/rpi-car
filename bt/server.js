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

stdin.addListener("data", function (d) {
  var input = d.toString().substring(0, d.length - 1);
  switch (input) {
    case "0":
      lastCommand = "run";
      break;
    case "1":
      lastCommand = "stop";
      break;

    case "2":
      lastCommand = "goForward:0.05";
      break;
    case "3":
      lastCommand = "goForward:0.1";
      break;
    case "4":
      lastCommand = "goForward:0.2";
      break;
    case "5":
      lastCommand = "goForward:0.3";
      break;

    case "6":
      lastCommand = "goBackward:0.05";
      break;
    case "7":
      lastCommand = "goBackward:0.1";
      break;
    case "8":
      lastCommand = "goBackward:0.2";
      break;
    case "9":
      lastCommand = "goBackward:0.3";
      break;

    default:
      lastCommand = "stop";
      break;
  }
  console.log("your command:", lastCommand);
  if (portOpen) port.write(new Buffer(lastCommand + '\r\n', 'utf-8'), function (err) {
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
  var input = data.toString().trim();
  console.log('received:', input);

  // handshake
  if (input == 'hello') {
    port.write(new Buffer(input + '\r\n', 'utf-8'), function (err) {
      if (err) {
        return console.log('err:', err);
      }
      console.log('sent:', input);
    });
  }
});

port.on('close', function () {
  portOpen = false;
  console.log('in port closed.');
});

port.on('error', function (err) {
  portOpen = false;
  console.log('in port error.', err);
});
