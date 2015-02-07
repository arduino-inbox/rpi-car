#!/usr/bin/env node

/*
 @todo
 - check what's up with pi blaster child process not sending output
 - handle sigterm and terminate child processes (pi blaster)
 - separate logging for each node (at least mute/unmute some nodes output using commands maybe)
 - check why command are not received from bt.
 */

var _ = require('lodash');
var async = require('async');
var events = require('events');
var winston = require('winston');

function Robot(config) {
  var self = this;
  self.name = 'Robot';
  self.config = config;
  self.nodes = {};
  self.started = (new Date()).getTime();

  self.uptime = function () {
    return (((new Date()).getTime() - self.started) / 1000).toFixed(4);
  };

  if (process.env.NODE_ENV == "daemon") {
    self.logger = new (winston.Logger)({
      transports: [
        new (winston.transports.File)({
          filename: '/var/log/car/info.log',
          level: 'info'
        })
      ],
      exceptionHandlers: [
        new winston.transports.File({
          filename: '/var/log/car/crash.log'
        })
      ]
    });
  } else {
    self.logger = new (winston.Logger)({
      transports: [
        new (winston.transports.Console)({
          colorize: 'all',
          level: (process.env.DEBUG ? 'debug' : 'info')
        })
      ]
    });
  }

  var configureNode = function (nodeName, done) {
    self.logger.info(self.uptime(), "Configuring " + nodeName);

    // Init node
    var node = new (require('./nodes/' + nodeName))(self.config.nodes[nodeName].config);

    // Log messages
    _.forEach(['debug', 'info', 'warning', 'error'], function (logLevel) {
      node.on(logLevel, function (message) {
        self.logger[logLevel](self.uptime(), logLevel, nodeName, message);
      });
    });

    self.nodes[nodeName] = node;
    done(null, nodeName);
  };

  var notifyAllNodes = function (message) {
    _.forEach(self.nodes, function (node) {
      node.emit(message);
    })
  };

  var goOnline = function () {
    if (self.online) return;
    self.online = true;
    self.logger.info(self.uptime(), "Online");
    notifyAllNodes("online");
  };

  //var goOffline = function () {
  //  self.online = false;
  //  self.logger.info(self.uptime(), "Offline");
  //  notifyAllNodes("offline");
  //  setTimeout(function () {
  //    process.exit();  // die to reconnect.
  //  }, self.config.nodes.transmitter.config.timeout);
  //};

  var standBy = function (done) {
    self.logger.info(self.uptime(), "Entering standby mode");
    self.nodes.transmitter.on("connected", function () {
      goOnline();
    });
    self.nodes.transmitter.on("error", function (err) {
      self.logger.error('Transmitter error.', err);
      process.exit();
    });
    // Bluetooth commands
    self.nodes.transmitter.on('data', function (data) {
      data = data.toString().trim();
      self.logger.info(self.uptime(), "data", "transmitter", data);

      data = data.split(":");
      var cmd = data[0];
      var speed = parseFloat(data[1] || self.config.nodes.motor.defaultSpeed);

      switch (cmd) {
        case "run":
          self.mode = "auto";
          break;
        case "goForward":
          self.mode = "manual";
          command("motor", "goForward", speed);
          break;
        case "goBackward":
          self.mode = "manual";
          command("motor", "goBackward", speed);
          break;
        default:
        case "stop":
          self.mode = "manual";
          command("motor", "stop");
          break;
      }
    });

    var command = function (nodeName, message, aux) {
      self.nodes[nodeName].emit("command", message, aux);
      self.nodes.transmitter.emit('transmit', self.uptime(), nodeName, "command", message + (aux ? ':' + aux : ''));
    };

    self.nodes.ultrasonic.on('update', function (distance) {
      self.nodes.transmitter.emit('transmit', self.uptime(), "ultrasonic", "distance", distance);
      if (self.mode != "auto") return;

      if (distance < 10) {
        command("motor", "goBackward");
      } else if (distance > 30) {
        command("motor", "goForward");
      } else {
        command("motor", "stop");
      }
    });

    done();
  };

  var configureNodes = function (done) {
    async.map(_.keys(self.config.nodes), configureNode, function (err, output) {
      if (err) return done(err);
      self.logger.debug(self.uptime(), "output", output);
      done();
    });
  };

  self.start = function () {
    async.waterfall([
      configureNodes,
      standBy
    ], function (err) {
      if (err) {
        return self.logger.error("error", self.uptime(), err);
      }
      notifyAllNodes("offline");
      self.logger.info(self.uptime(), "Ready");
    });
  };
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

// Start
var config = {
  nodes: {
    transmitter: {
      config: {
        address: '60:FB:42:7B:23:54', //'70:73:CB:C3:66:98', // @todo config
        channel: 3,
        timeout: 30 * 1000
      }
    },
    ultrasonic: {
      config: {
        echoPin: constants.pins.PIN_ULTRASONIC_ECHO,
        triggerPin: constants.pins.PIN_ULTRASONIC_TRIG,
        timeout: 1000, // values smaller than 500 always return -1
        interval: 50 // @todo to fiddle with
      }
    },
    motor: {
      config: {
        speedPin: constants.pins.PIN_MOTOR_SPEED_PWM,
        directionPin1: constants.pins.PIN_MOTOR_DIR1,
        directionPin2: constants.pins.PIN_MOTOR_DIR2,
        defaultSpeed: 0.3,
        maxSpeed: 0.5
      }
    }
  }
};

var startRobot = function () {
  var robot = new Robot(config);
  robot.start();
  // @todo fixme reset the robot on disconnect.
};
startRobot();

