var events = require('events');
var mpu6050 = require('mpu6050');
var microtime = require('microtime');

function Gyro(config) {

  var self = this;

  self.config = config;
  self.sensor = new mpu6050();
  self.sensor.initialize();

  var t = microtime.now();
  self.acceleration = {x: 0, y: 0, z: 0, dt: 0, t: t};
  self.rotation = {x: 0, y: 0, z: 0, dt: 0, t: t};

  events.EventEmitter.call(self);

  // private
  var update = function () {
    self.sensor.getMotion6(function (err, data) {
      if (err) {
        self.emit('error', err || 'Could not get motion data.');
      }

      var t = microtime.now();
      self.measurements = {
        acceleration: {
          x: data[0],
          y: data[1],
          z: data[2]
        },
        rotation: {
          x: data[3],
          y: data[4],
          z: data[5]
        },
        time: {
          dt: t - self.time.t,
          t: t
        }
      };
      self.emit('update', self.measurements);

      // Continuous updates
      if (self.online) {
        update();
      }
    });
  };

  self.sensor.testConnection(function (err, testPassed) {
    if (err || !testPassed) {
      return self.emit('error', err || 'Could not connect to gyro.');
    }

    self.emit("info", "Gyro standing by.");

    self.on('online', function () {
      self.online = true;
      update();
    });

    self.on('offline', function () {
      self.online = false;
    });
  });
}
Gyro.prototype.__proto__ = events.EventEmitter.prototype;

module.exports = Gyro;
