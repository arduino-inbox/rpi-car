var events = require('events');

function Robot(config) {
  var self = this;
  self.name = 'Robot';
  self.config = config;
  self.nodes = [];
  self.started = (new Date()).getTime();
  self.uptime = function () {
    return (((new Date()).getTime() - self.started) / 1000).toFixed(4);
  };
  self.logger = console; // @todo better logger

  self.logger.log("Configuring nodes");
  self.config.nodes.forEach(function (node) {
    self.logger.log("-", node.name);
    var nodeClass = require('./nodes/' + node.name);
    var nodeInstance = new nodeClass(self, node.config);
    self.nodes.push({
      name: node.name,
      instance: nodeInstance
    });
  });

  self.work = function () {
    self.logger.log("Starting nodes");
    self.nodes.forEach(function (node) {
      self.logger.log("-", node.name);
      node.instance.on('update', function (param, value) {
        self.emit('nodeUpdate', self.uptime(), node.name, param, value);
        self.logger.log("[", self.uptime(), "]", "update", node.name, "", param, "", value);
      });
      node.instance.on('info', function (message) {
        self.logger.log("[", self.uptime(), "]", "info", node.name, "", message);
      });
      node.instance.on('error', function (message) {
        self.logger.log("[", self.uptime(), "]", "error", node.name, "", message);
        process.exit();
      });
      node.instance.work();
    });

    // simple behaviour
    var reactToFrontDistance = function (frontDistance) {
      if (frontDistance < 10) {
        self.emit('goBackward'); // @todo pass the speed
      }  else if (frontDistance > 30) {
        self.emit('goForward'); // @todo pass the speed
      } else {
        self.emit('stop');
      }
    };
    self.on('frontDistance', reactToFrontDistance);
  }
}
Robot.prototype.__proto__ = events.EventEmitter.prototype;

// @todo add more constants from other nodes (e.g. bt client config)
// @todo move to config file
var constants = {
  pins: {
    PIN_MOTOR_SPEED_PWM: 25,
    PIN_MOTOR_DIR1: 17,
    PIN_MOTOR_DIR2: 27,
    PIN_ULTRASONIC_TRIG: 24,
    PIN_ULTRASONIC_ECHO: 22,
    PIN_ULTRASONIC_SERVO: 18,
    PIN_STEERING_SERVO: 23
  }
};

// Run
var robot = new Robot({
  nodes: [
    {
      name: "transmitter", // this one should start first.
      config: {
        address: '60:FB:42:7B:23:54', //'70:73:CB:C3:66:98', // @todo config
        channel: 3
      }
    },
    {
      name: "ultrasonic",
      config: {
        echoPin: constants.pins.PIN_ULTRASONIC_ECHO,
        triggerPin: constants.pins.PIN_ULTRASONIC_TRIG,
        timeout: 1000, // values smaller than 500 always return -1
        interval: 50 // @todo to fiddle with
      }
    },
    {
      name: "motor",
      config: {
        speedPin: constants.pins.PIN_MOTOR_SPEED_PWM,
        directionPin1: constants.pins.PIN_MOTOR_DIR1,
        directionPin2: constants.pins.PIN_MOTOR_DIR2,
        defaultSpeed: 0.3
      }
    }
  ]
});

robot.work();
