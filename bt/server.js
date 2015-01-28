#! /usr/bin/env node

var serialport = require("serialport");
var SerialPort = serialport.SerialPort;

var portName = "/dev/cu.Bluetooth-Incoming-Port";
var port = new SerialPort(portName, {
  baudRate: 115200
});
var message = 'ack\r\n';

port.on('open', function () {
  console.log('port open. rate: ', port.options.baudRate);
});

port.on('data', function (data) {
  console.log('received:', data.toString());
  port.write(message, function(err) {
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
