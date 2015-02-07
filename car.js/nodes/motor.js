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
    if (!speed) speed = self.config.defaultSpeed;
    if (speed > self.config.maxSpeed) speed = self.config.maxSpeed;
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

  child.exec('killall pi-blaster', function () {
    self.piBlasterProc = child.exec('pi-blaster');
    if (!self.piBlasterProc.pid) {
      return self.emit('error', "Could not start pi-blaster");
    }

    self.emit('info', ["pi-blaster PID:", self.piBlasterProc.pid]);
    self.piBlasterProc.on('close', function (code, signal) {
      self.emit("error", "pi-blaster exited with code " + code + " on " + signal + " signal.");
    });
    self.emit("info", "Motor standing by.");
  });

  var onCommand = function (cmd, data) {
    self.emit('debug', ["oncommand", cmd, data]);
    switch (cmd) {
      case "goForward":
        goForward(data);
        break;
      case "goBackward":
        goBackward(data);
        break;
      default:
      case "stop":
        stop();
        break;
    }
  };

  self.on('online', function () {
    self.on('command', onCommand);
  });

  self.on('offline', function () {
    self.removeAllListeners('command');
  });
}

Motor.prototype.__proto__ = events.EventEmitter.prototype;
module.exports = Motor;
