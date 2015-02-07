#! /usr/bin/env node

var serialport = require("serialport");
var SerialPort = serialport.SerialPort;

var portName = "/dev/cu.Bluetooth-Incoming-Port";
var port = new SerialPort(portName, {
  baudRate: 115200
});
var lastCommand = "stop";


var express = require("express");
var app = express();
var httpPort = 1337;

app.use(express.static(__dirname + '/public'));
app.set('views', __dirname + '/views');
app.set('view engine', "ejs");
app.engine('ejs', require('ejs').__express);

app.get("/", function (req, res) {
  res.render("index");
});

var io = require('socket.io').listen(app.listen(httpPort));
io.sockets.on('connection', function (socket) {
  socket.emit('message', {message: 'Welcome!'});
  socket.on('send', function (data) {
    io.sockets.emit('message', data);

    port.write(new Buffer(lastCommand + '\r\n', 'utf-8'), function (err) {
      if (err) {
        io.sockets.emit('message', 'Could not send '+lastCommand+' command. Error: '+err);
      }
    });
  });
});

port.on('open', function () {
  io.sockets.emit('message', 'port open. rate: ' + port.options.baudRate);
});

port.on('data', function (data) {
  var input = data.toString().trim();
  io.sockets.emit('message', 'received:'+input);

  // handshake
  if (input == 'hello') {
    port.write(new Buffer(input + '\r\n', 'utf-8'), function (err) {
      if (err) {
        return io.sockets.emit('message', 'Could not send '+input+' command. Error: '+err);
      }
      io.sockets.emit('message', 'sent:'+input);
    });
  }
});

port.on('close', function () {
  io.sockets.emit('message', 'serial port closed.');
});

port.on('error', function (err) {
  io.sockets.emit('message', 'serial port error. '+err);
});

console.log("Listening on port " + httpPort);
