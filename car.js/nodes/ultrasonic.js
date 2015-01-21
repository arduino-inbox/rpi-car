module.exports = function (config) {
  var usonic = require('r-pi-usonic');
  var self = this;
  self.config = config || {
    echoPin: 22,
    triggerPin: 24,
    timeout: 1000
  };
  self.sensor = usonic.sensor(self.config.echoPin, self.config.triggerPin, self.config.timeout);

  return {
    getDistance: function () {
      return self.sensor();
    }
  }
};
