var events = require('events');
var piblaster = require('pi-blaster.js');
var onoff = require('onoff');

function Motor(robot, config) {

  var self = this;

  self.robot = robot;
  self.config = config;
  self.defaultSpeed = self.config.defaultSpeed;
  self.directionPin1 = new onoff.Gpio(self.config.directionPin1, 'out');
  self.directionPin2 = new onoff.Gpio(self.config.directionPin2, 'out');

  events.EventEmitter.call(self);

  var setSpeed = function (speed) {
    if (speed > 1) speed = 1;
    if (speed < 0) speed = 0;

    self.emit('info', ['setting speed to', speed]);

    piblaster.setPwm(self.config.speedPin, speed);
  };

  // private
  var goForward = function (speed) {
    self.emit('info', 'received "goForward" command.');

    self.directionPin1.writeSync(1);
    self.directionPin2.writeSync(0);

    setSpeed(speed || self.defaultSpeed);
  };

  var goBackward = function (speed) {
    self.emit('info', 'received "goBackward" command.');

    self.directionPin1.writeSync(0);
    self.directionPin2.writeSync(1);

    setSpeed(speed || self.defaultSpeed);
  };

  var stop = function () {
    self.emit('info', 'received "stop" command.');

    self.directionPin1.writeSync(0);
    self.directionPin2.writeSync(0);

    setSpeed(0);
  };

  // public
  self.work = function () {
    self.robot.on('goBackward', goBackward);
    self.robot.on('goForward', goForward);
    self.robot.on('stop', stop);
  }
}

Motor.prototype.__proto__ = events.EventEmitter.prototype;
module.exports = Motor;
