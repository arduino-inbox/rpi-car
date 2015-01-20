#! /usr/bin/env node

var serialport = require("serialport");
var SerialPort = serialport.SerialPort;

var portName = "/dev/cu.Bluetooth-Incoming-Port";
var port = new SerialPort(portName, {
  baudRate: 57600
});
var message = 'pong\r\n';

port.on('open', function () {
  console.log('port open. rate: ', port.options.baudRate);
});

port.on('data', function (data) {
  console.log('[' + (new Date()).getTime() + ']', 'received:', data.toString());
  port.write(message, function(err) {
    console.log('[' + (new Date()).getTime() + ']', 'sent:', message);
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
