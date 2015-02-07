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
var socket = {
  emit: function () {}  // dummy
};

io.sockets.on('connection', function (s) {
  socket = {
    emit: function (t, m) {
      s.emit(t, m);
      if (process.env.DEBUG) {
        console.log("socket.emit", t, m);
      }
    }
  };
  socket.emit('message', 'Welcome!');
  s.on('send', function (data) {
    lastCommand = data.trim();
    socket.emit('message', {info: data});

    port.write(new Buffer(lastCommand + '\r\n', 'utf-8'), function (err) {
      if (err) {
        socket.emit('message', {error: 'Could not send '+lastCommand+' command. Error: '+err});
      }
    });
  });
});

port.on('open', function () {
  socket.emit('message', {info: 'port open. rate: ' + port.options.baudRate});
});

port.on('data', function (data) {
  var input = data.toString().trim();
  // socket.emit('message', 'received:'+input);
  // '13.2430:ultrasonic:distance:53.4691724137931'
  var inputData = input.split(':');
  socket.emit('runtime', inputData[0]);
  socket.emit('message', {input: {
    sensor: inputData[1],
    parameter: inputData[2],
    value: inputData[3]
  }});

  // handshake
  if (input == 'hello') {
    port.write(new Buffer(input + '\r\n', 'utf-8'), function (err) {
      if (err) {
        return socket.emit('message', {error: 'Could not send '+input+' command. Error: '+err});
      }
      socket.emit('message', {info: 'sent:'+input});
    });
  }
});

port.on('close', function () {
  socket.emit('message', {error: 'serial port closed.'});
});

port.on('error', function (err) {
  socket.emit('message', {error: 'serial port error. '+err});
});

console.log("Listening on port " + httpPort);
