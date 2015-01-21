module.exports = function (config) {
  var usonic = require('r-pi-usonic');
  var events = require('events');
  var self = this;

  self.config = config;
  self.sensor = usonic.sensor(self.config.echoPin, self.config.triggerPin, self.config.timeout);
  self.distance = 2^16 - 1;

  events.EventEmitter.call(self);

  var update = function () {
    self.distance = self.sensor();
    self.emit('update', 'distance', self.distance);
  };

  return {
    work: function () {
      setInterval(update, self.config.interval);
    }
  }
};
