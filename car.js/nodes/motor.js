var events = require('events');
var piBlasterJs = require('pi-blaster.js');
var onoff = require('onoff');
var child = require('child_process');

function Motor(config) {

  var self = this;

  self.config = config;
  self.defaultSpeed = self.config.defaultSpeed;
  self.directionPin1 = new onoff.Gpio(self.config.directionPin1, 'out');
  self.directionPin2 = new onoff.Gpio(self.config.directionPin2, 'out');

  events.EventEmitter.call(self);

  var setSpeed = function (speed) {
    if (speed > 1) speed = 1;
    if (speed < 0) speed = 0;

    self.emit('debug', ['Setting speed to', speed]);

    piBlasterJs.setPwm(self.config.speedPin, speed);
  };

  // private
  var goForward = function (speed) {
    self.emit('debug', 'received "goForward" command.');
    if (self.direction == "forward") {
      self.emit('debug', 'already executing "goForward" command.');
      return;
    }
    self.emit('debug', 'executing "goForward" command.');
    self.direction = "forward";

    self.directionPin1.writeSync(1);
    self.directionPin2.writeSync(0);

    setSpeed(speed);
  };

  var goBackward = function (speed) {
    self.emit('debug', 'received "goBackward" command.');
    if (self.direction == "backward") {
      self.emit('debug', 'already executing "goBackward" command.');
      return;
    }
    self.emit('debug', 'executing "goBackward" command.');
    self.direction = "backward";

    self.directionPin1.writeSync(0);
    self.directionPin2.writeSync(1);

    setSpeed(speed);
  };

  var stop = function () {
    self.emit('debug', 'received "stop" command.');
    if (!self.direction) {
      self.emit('debug', 'already executing "stop" command.');
      return;
    }
    self.emit('debug', 'executing "stop" command.');
    self.direction = null;

    self.directionPin1.writeSync(0);
    self.directionPin2.writeSync(0);

    setSpeed(0);
  };

  // @todo test
  self.piBlasterProc = child.spawn('pi-blaster');
  self.piBlasterProc.stdout.on('data', function (data) {
    self.emit("info", "pi-blaster::stdout: " + data);
  });
  self.piBlasterProc.stderr.on('data', function (data) {
    self.emit("error", "pi-blaster::stderr: " + data);
  });
  self.piBlasterProc.on('close', function (code, signal) {
    self.emit("error", "pi-blaster exited with code " + code + " on " + signal + " signal.");
  });

  self.emit("info", "Motor standing by.");

  self.on('online', function () {
    self.on('goBackward', goBackward);
    self.on('goForward', goForward);
    self.on('stop', stop);
  });

  self.on('offline', function () {
    self.removeAllListeners('goBackward');
    self.removeAllListeners('goForward');
    self.removeAllListeners('stop');
  });
}

Motor.prototype.__proto__ = events.EventEmitter.prototype;
module.exports = Motor;
