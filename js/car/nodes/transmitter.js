var _ = require('lodash');
var events = require('events');
var bt = require('bluetooth-serial-port');

// @note Do not emit "error". Use "disconnected" instead.

function Transmitter(config) {

  var self = this;

  self.config = config;
  self.btSerial = new bt.BluetoothSerialPort();

  events.EventEmitter.call(self);

  var transmit = function (uptime, nodeName, param, value) {
    var message = uptime + ':' + nodeName + ':' + param + ':' + value;
    self.btSerial.write(new Buffer(message, 'utf-8'), function (err) {
      self.emit('debug', ['sent', message]);
      if (err) {
        self.emit('disconnected', ['transmission failed. could not send message.', err.message]);
      }
    });
  };

  var connect = function () {
    self.emit('info', 'Connecting to server.');

    // Wait for channel
    self.channelFound = false;
    var waitForChannel = function () {
      if (!self.channelFound) {
        return self.emit('disconnected', 'Channel lookup timeout.');
      }
    };
    setTimeout(waitForChannel, self.config.timeout);

    // Handshake flag (called below)
    var waitForHandshake = function () {
      if (!self.handshakeReceived) {
        return self.emit('disconnected', 'Handshake response timeout.');
      }
    };

    var receiveHandshake = function (data) {
      data = data.toString().trim();
      self.emit("debug", ["Receive handshake", data, data == 'hello']);

      // On handshake response
      if (data == 'hello') {
        self.handshakeReceived = true;  // This will save us from handshake timeout error.
        self.btSerial.removeListener('data', receiveHandshake);
        self.emit('connected');  // Emit "connected" event for robot to go online.
      }
    };

    var sendHandshake = function () {
      // Reset flag
      self.handshakeReceived = false;

      // Subscribe to data while handshaking
      self.btSerial.on('data', receiveHandshake);

      // Send hello
      self.btSerial.write(new Buffer('hello', 'utf-8'), function (err) {
        self.emit('debug', ['sent', 'hello']);
        if (err) {
          return self.emit('disconnected', ['transmission failed. could not send "hello".', err.message]);
        }
        setTimeout(waitForHandshake, 5 * 1000);
      });
    };

    // Port lookup
    self.btSerial.findSerialPortChannel(
      self.config.address,
      function (channel) {
        self.emit('debug', ['Bluetooth serial port channel found.', channel]);
        if (channel == self.config.channel) {
          self.channelFound = true;
          self.emit('info', ['This is the bluetooth serial port channel we are looking for.']);

          // Try to connect
          self.btSerial.connect(
            self.config.address,
            self.config.channel,
            function () {
              self.emit('info', 'Bluetooth connected.');

              // Send handshake
              sendHandshake();
            },
            function (err) {
              self.emit('disconnected', ['Cannot connect.', err]);
            }
          );
        }
      },
      function () {
        self.emit('disconnected', ['Cannot find a serial port channel on ' + self.config.address + '.']);
      }
    );
    self.btSerial.inquire();
  };

  self.emit("info", "Transmitter standing by.");

  self.on("connect", function () {
    self.emit('offline');
    connect();
  });

  self.on("offline", function () {
    self.removeAllListeners('transmit');
    self.btSerial.removeAllListeners('data');
  });

  self.on("online", function () {
    self.on('transmit', transmit);
    self.btSerial.on('data', function (data) {
      self.emit('data', data.toString());
    });
  });
}

Transmitter.prototype.__proto__ = events.EventEmitter.prototype;
module.exports = Transmitter;
