var events = require('events');
var usonic = require('r-pi-usonic');

function Ultrasonic(config) {

  var self = this;

  self.config = config;
  self.sensor = usonic.createSensor(self.config.echoPin, self.config.triggerPin, self.config.timeout);
  self.distance = 2^16 - 1;

  events.EventEmitter.call(self);

  // private
  var update = function () {
    self.distance = self.sensor();
    self.emit('frontDistance', self.distance);
  };

  self.emit("info", "Ultrasonic standing by.");
  self.on('online', function () {
    self.worker = setInterval(update, self.config.interval);
  });
  self.on('offline', function () {
    clearInterval(self.worker);
  });
}
Ultrasonic.prototype.__proto__ = events.EventEmitter.prototype;

module.exports = Ultrasonic;
