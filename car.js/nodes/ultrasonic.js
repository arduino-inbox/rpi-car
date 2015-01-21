module.exports = function (config) {
  var usonic = require('r-pi-usonic');
  var self = this;

  self.echoPin = config.echoPin || 22;
  self.triggerPin = config.triggerPin || 24;
  self.timeout = config.timeout || 200;
  self.delay = config.delay || 30;
  self.sensor = usonic.sensor(self.echoPin, self.triggerPin, self.timeout);

  return {
    getDistance: function () {
      return self.sensor();
    }
  }
};
