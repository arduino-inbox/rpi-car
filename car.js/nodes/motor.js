var events = require('events');
var piblaster = require('pi-blaster.js');
var onoff = require('onoff');

function Motor(robot, config) {

  var self = this;

  self.robot = robot;
  self.config = config;
  self.defaultSpeed = 1000; // @todo to fiddle with
  self.directionPin1 = new onoff.Gpio(self.config.directionPin1, 'out');
  self.directionPin2 = new onoff.Gpio(self.config.directionPin2, 'out');

  events.EventEmitter.call(self);

  var setSpeed = function (speed) {
    piblaster.setPwm(self.config.speedPin, speed);
  };

  // private
  var goForward = function (speed) {
    self.directionPin1.writeSync(1);
    self.directionPin2.writeSync(0);

    setSpeed(speed || self.defaultSpeed);
  };

  var goBackward = function (speed) {
    self.directionPin1.writeSync(0);
    self.directionPin2.writeSync(1);

    setSpeed(speed || self.defaultSpeed);
  };

  var stop = function () {
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
