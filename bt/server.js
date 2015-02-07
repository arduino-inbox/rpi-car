#! /usr/bin/env node

var express = require("express");
var app = express();
var port = 1337;

app.use(express.static(__dirname + '/public'));
app.set('views', __dirname + '/views');
app.set('view engine', "ejs");
app.engine('ejs', require('ejs').__express);

app.get("/", function(req, res){
  res.render("index");
});

var io = require('socket.io').listen(app.listen(port));
io.sockets.on('connection', function (socket) {
  socket.emit('message', { message: 'Welcome!' });
  socket.on('send', function (data) {
    io.sockets.emit('message', data);
  });
});


console.log("Listening on port " + port);

//var serialport = require("serialport");
//var SerialPort = serialport.SerialPort;
//
//var portName = "/dev/cu.Bluetooth-Incoming-Port";
//var port = new SerialPort(portName, {
//  baudRate: 115200
//});
//var sys = require("sys");
//var stdin = process.openStdin();
//
//var lastCommand = "stop";
//
//stdin.addListener("data", function (d) {
//  var input = d.toString().substring(0, d.length - 1);
//  switch (input) {
//    case "0":
//      lastCommand = "run";
//      break;
//    case "1":
//      lastCommand = "stop";
//      break;
//
//    case "2":
//      lastCommand = "goForward:0.05";
//      break;
//    case "3":
//      lastCommand = "goForward:0.1";
//      break;
//    case "4":
//      lastCommand = "goForward:0.2";
//      break;
//    case "5":
//      lastCommand = "goForward:0.3";
//      break;
//
//    case "6":
//      lastCommand = "goBackward:0.05";
//      break;
//    case "7":
//      lastCommand = "goBackward:0.1";
//      break;
//    case "8":
//      lastCommand = "goBackward:0.2";
//      break;
//    case "9":
//      lastCommand = "goBackward:0.3";
//      break;
//
//    default:
//      lastCommand = "stop";
//      break;
//  }
//  console.log("command:", lastCommand);
//  port.write(new Buffer(lastCommand + '\r\n', 'utf-8'), function (err) {
//    if (err) {
//      console.log('err ' + err);
//    }
//  });
//});
//
//port.on('open', function () {
//  console.log('port open. rate: ', port.options.baudRate);
//});
//
//port.on('data', function (data) {
//  var input = data.toString().trim();
//  console.log('received:', input);
//
//  // handshake
//  if (input == 'hello') {
//    port.write(new Buffer(input + '\r\n', 'utf-8'), function (err) {
//      if (err) {
//        return console.log('err:', err);
//      }
//      console.log('sent:', input);
//    });
//  }
//});
//
//port.on('close', function () {
//  console.log('in port closed.');
//});
//
//port.on('error', function (err) {
//  console.log('in port error.', err);
//});
