var events = require('events');
var usonic = require('r-pi-usonic');

function Ultrasonic(robot, config) {

  var self = this;

  self.robot = robot;
  self.config = config;
  self.sensor = usonic.sensor(self.config.echoPin, self.config.triggerPin, self.config.timeout);
  self.distance = 2^16 - 1;

  events.EventEmitter.call(self);

  // private
  var update = function () {
    self.distance = self.sensor();
    self.emit('update', 'distance', self.distance);
    self.robot.emit('frontDistance', self.distance);
  };

  // public
  self.work = function () {
    setInterval(update, self.config.interval);
  }
}
Ultrasonic.prototype.__proto__ = events.EventEmitter.prototype;

module.exports = Ultrasonic;