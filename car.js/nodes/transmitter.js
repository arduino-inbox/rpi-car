var events = require('events');
var bt = require('bluetooth-serial-port');

function Transmitter(robot, config) {

  var self = this;

  self.robot = robot;
  self.config = config;
  self.btSerial = new bt.BluetoothSerialPort();

  events.EventEmitter.call(self);


  self.btSerial.connect(self.config.address, self.config.channel, function () {
    self.emit('info', 'connected');
    self.connected = true;

    self.btSerial.on('data', function (data) {
      self.emit('info', ['received', data.toString()]);
    });
  }, function () {
    throw new Error('cannot connect');
  });
  self.btSerial.inquire();

  var transmit = function (uptime, nodeName, param, value) {
    if (!self.connected) {
      self.robot.removeListener('nodeUpdate', transmit);

      return self.emit('info', 'transmission failed. not connected.');
    }

    var message = uptime+':'+nodeName+':'+param+':'+value;
    self.btSerial.write(new Buffer(message, 'utf-8'), function (err) {
      self.emit('info', ['sent', message]);
      if (err) {
        self.emit('info', ['transmission failed. error occurred.', err.message]);
      }
    });
  };

  // public
  self.work = function () {
    self.robot.on('nodeUpdate', transmit);
  }
}

Transmitter.prototype.__proto__ = events.EventEmitter.prototype;
module.exports = Transmitter;
