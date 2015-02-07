var events = require('events');
var bt = require('bluetooth-serial-port');

function Transmitter(config) {

  var self = this;

  self.config = config;
  self.btSerial = new bt.BluetoothSerialPort();

  events.EventEmitter.call(self);

  var transmit = function (uptime, nodeName, param, value) {
    var message = uptime+':'+nodeName+':'+param+':'+value;
    self.btSerial.write(new Buffer(message, 'utf-8'), function (err) {
      self.emit('debug', ['sent', message]);
      if (err) {
        self.emit('error', ['transmission failed. error occurred.', err.message]);
      }
    });
  };

  var connect = function () {
    self.emit('info', 'Connecting to server.');
    self.btSerial.connect(self.config.address, self.config.channel, function () {
      self.btSerial.write(new Buffer('hello', 'utf-8'), function (err) {
        self.emit('debug', ['sent', 'hello']);
        if (err) {
          return self.emit('error', ['transmission failed. error occurred.', err.message]);
        }
        self.emit('info', 'Connected.');
        self.emit('connected');
      });
    }, function () {
      self.emit('error', 'Cannot connect.');
      if (self.config.reconnect) {
        setTimeout(connect, self.config.reconnectTimeout);
      }
    });
    self.btSerial.inquire(); // @todo check if we need to run self.btSerial.inquire(); each time
  };

  self.emit("info", "Transmitter standing by.");
  self.on("offline", function () {
    self.removeAllListeners('transmit');
    self.btSerial.removeAllListeners('data');
    connect();
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
